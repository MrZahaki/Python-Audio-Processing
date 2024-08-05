class AudioMetadataDatabase:
    def __init__(self):
        self.records = {}

    def add_record(self, record):
        self.records[record.name] = record

    def get_record(self, name):
        return self.records.get(name)

    def remove_record(self, name):
        if name in self.records:
            del self.records[name]

    def index(self):
        return list(self.records.keys())

    def __getitem__(self, name):
        return self.get_record(name)

    def __setitem__(self, name, record):
        self.add_record(record)