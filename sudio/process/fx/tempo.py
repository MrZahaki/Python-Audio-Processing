# SUDIO - Audio Processing Platform
# Copyright (C) 2024 Hossein Zahaki

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

# - GitHub: https://github.com/MrZahaki/sudio


from sudio.process.fx import FX
from  sudio._process_fx_tempo import tempo_cy
from sudio.io import SampleFormat
import numpy as np

class Tempo(FX):
    def __init__(self, *args, **kwargs) -> None:
        """
        Initialize the Tempo audio effect processor for time stretching.

        Configures time stretching with support for both streaming and offline 
        audio processing, optimized for 32-bit floating-point precision.

        Parameters:
        -----------
        *args : Variable positional arguments
            Arguments for parent FX class initialization.

        **kwargs : Variable keyword arguments
            Additional configuration parameters for tempo processing.

        Notes:
        ------
        Implements advanced time stretching using WSOLA (Waveform Similarity 
        Overlap-Add) algorithm to modify audio tempo without altering pitch.
        """
        features = {
            'streaming_feature': True, 
            'offline_feature': True,
            'preferred_datatype': SampleFormat.FLOAT32
            }
        super().__init__(*args, **kwargs, **features)

    def process(self, data: np.ndarray, tempo:float=1.0, **kwargs):
        """
        Time stretch audio without changing its pitch.

        Applies tempo modification using an improved WSOLA algorithm, 
        allowing precise control over audio playback speed.

        Parameters:
        -----------
        data : numpy.ndarray
            Input audio data. Supports mono and multi-channel arrays.

        tempo : float, optional
            Tempo scaling factor:
            - 1.0 (default): Original tempo
            - 2.0: Double speed
            - 0.5: Half speed

        **kwargs : dict, optional
            Additional processing parameters (ignored in this implementation)

        Returns:
        --------
        numpy.ndarray
            Time-stretched audio data with preserved original data type.

        Processing Details:
        ------------------
        - Maintains original audio quality
        - Preserves spectral characteristics
        - Supports variable tempo scaling
        - Handles both single and multi-channel audio

        Examples:
        ---------
        >>> import numpy as np
        >>> from sudio.process.fx import Tempo
        >>> audio_data = np.random.randn(44100)  # Example audio
        >>> tempo_fx = Tempo()
        >>> stretched_audio = tempo_fx.process(audio_data, tempo=1.5)  # 1.5x speed
        """
        dtype = data.dtype
        data = tempo_cy(data, tempo, self._sample_rate)
        return data.astype(dtype)
    
    