# the name of allah
# import multiprocessing
import threading
import queue
import time


class Pipeline(threading.Thread):
    # type LiveProcessing, DeadProcessing or timeout value
    def __init__(self, max_size=None, io_buffer_size=10, pipe_type='LiveProcessing'):
        super(Pipeline, self).__init__(daemon=True)
        # self.manager = threading.Manager()
        # self.namespace = manager.Namespace()
        self._pipeline = []
        self.io_buffer_size = io_buffer_size
        self.input_line = queue.Queue(maxsize=io_buffer_size)
        self.output_line = queue.Queue(maxsize=io_buffer_size)
        self.max_size = max_size
        self.pipe_type = pipe_type
        self.refresh_ev = threading.Event()
        self.init_queue = queue.Queue()
        # block value, timeout
        if pipe_type == 'LiveProcessing':
            self._process_type = (False, None)
        elif pipe_type == 'DeadProcessing':
            self._process_type = (True, None)
        elif type(pipe_type) == float:
            self._process_type = (True, pipe_type)
        else:
            raise ValueError

        self.put = self.__call__
        self.get = self.output_line.get
        self.put_nowait = self.input_line.put_nowait
        self.get_nowait = self.output_line.get_nowait
    def __call__(self, data):
        self.input_line.put(data, block=self._process_type[0], timeout=self._process_type[1])

    def clear(self):
        while not self.input_line.empty():
            self.input_line.get()
        while not self.output_line.empty():
            self.output_line.get()

    def run(self):
        while 1:
            try:
                while 1:
                    if self.refresh_ev.is_set():
                        while not self.init_queue.empty():
                            #init
                            self.init_queue.get()(self)
                        self.refresh_ev.clear()
                    # call from pipeline
                    ret_val = self._pipeline[0][0](*self._pipeline[0][1:], self.input_line.get_nowait())
                    for i in self._pipeline[1:]:
                        ret_val = i[0](*i[1:], ret_val)
                    self.output_line.put(ret_val, block=self._process_type[0], timeout=self._process_type[1])


            except IndexError:
                while not len(self._pipeline):
                    self.output_line.put(self.input_line.get(), block=self._process_type[0], timeout=self._process_type[1])
                    if self.refresh_ev.is_set():
                        while not self.init_queue.empty():
                            #init
                            self.init_queue.get()(self)
                        self.refresh_ev.clear()
            except (queue.Full, queue.Empty):
                pass

    def insert(self, index, func, args=(), init=()):

        if self.max_size:
            assert len(self._pipeline) + 1 < self.max_size
        if len(init):
            self.init_queue.put(init[0])
            self.refresh_ev.set()
            while self.refresh_ev.is_set(): pass
        self._pipeline.insert(index, [func, *args])
        return self

    def append(self, *func, args=(), init=()):
        """append new functions to pipeline

        Parameters
        ----------
        func : list or object
            Functions to be added to the pipe
        args: tuple
            Input Arguments of Functions
        init: tuple
            Initial functions(access to pipeline shared memory)

        Returns
        -------
        y : current object


        Examples
        --------
        Simple operations:

        >>> from scipy.signal import upfirdn
        >>> h = firwin(30, 8000, fs=72000)
        >>>
        >>> def simple_sum(x, y):
        >>>     return x + y
        >>> pip = Pipeline().append(upfirdn, simple_sum, args=((h), (2)))
        """
        if self.max_size:
            assert len(self._pipeline) + len(func) < self.max_size

        for i in init:
            if i:
                self.init_queue.put(i)
                self.refresh_ev.set()
            while self.refresh_ev.is_set(): pass

        for num, i in enumerate(func):
            try:
                self._pipeline.append([i, *args[num]])
            except IndexError:
                self._pipeline.append([i])
        return self

    def __delitem__(self, key):
        self.input_line.empty()
        del self._pipeline[key]

    def __len__(self):
        return len(self._pipeline)

    def __getitem__(self, key):
        try:
            assert type(key) == slice
            # indices = key.indices(len(self._pipeline))
            return Pipeline(max_size=self.max_size, io_buffer_size=self.io_buffer_size, pipe_type=self.pipe_type).append(*self._pipeline[key])
        except AssertionError:
            return  self._pipeline[key]


