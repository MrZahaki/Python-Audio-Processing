#  W.T.A
#  SUDIO (https://github.com/MrZahaki/sudio)
#  The Audio Processing Platform
#  Mail: mrzahaki@gmail.com
#  Software license: "Apache License 2.0". See https://choosealicense.com/licenses/apache-2.0/

from sudio.io import codec, SampleFormat
import base64

class WebAudioIO:
    """
    Web-based Audio I/O class for environments without native device support
    """
    @staticmethod
    def is_web_audio_supported() -> bool:
        try:
            from IPython.core.interactiveshell import InteractiveShell

            if InteractiveShell.initialized():
                InteractiveShell.instance()
            else:
                raise
        except:
            return False
        return True


    @staticmethod
    def play_audio_data(data: bytes, sample_format: SampleFormat, channels: int, frame_rate: int) -> bool:
        """
        Play audio data by creating an HTML5 audio element
        
        Parameters:
        -----------
        data : bytes
            Raw audio data
        sample_format : SampleFormat
            Sample format from sudio.SampleFormat
        channels : int
            Number of channels
        frame_rate : int
            Sample rate in Hz
            
        Returns:
        --------
        bool
            True if playback was successful
        """
        try:
            wav_data = codec.encode_to_mp3(
                data,
                format=sample_format,
                nchannels=channels,
                sample_rate=frame_rate
            )
            
            base64_data = base64.b64encode(wav_data).decode('ascii')
            audio_html = f"""
                <audio controls="controls" autoplay="autoplay">
                    <source src="data:audio/wav;base64,{base64_data}" type="audio/mp3" />
                    Your browser does not support the audio element.
                </audio>
            """
            
            # IPython environment
            from IPython.display import display, HTML
            display(HTML(audio_html))
            return True
            
        except:
            return False
        
        