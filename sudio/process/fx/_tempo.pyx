# distutils: language=c++
# cython: language_level=3


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



import numpy as np
cimport numpy as np
cimport cython
from libc.math cimport sqrt, pow, log2
from libc.string cimport memcpy
from libcpp cimport bool

DEF DEFAULT_SEQUENCE_MS = 82
DEF DEFAULT_SEEKWINDOW_MS = 28  
DEF DEFAULT_OVERLAP_MS = 12

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef np.ndarray tempo_cy(
    np.ndarray input_audio,
    float tempo,
    int sample_rate=44100,
    int sequence_ms=DEFAULT_SEQUENCE_MS,
    int seekwindow_ms=DEFAULT_SEEKWINDOW_MS, 
    int overlap_ms=DEFAULT_OVERLAP_MS):
    """
    Time stretch audio without changing pitch using WSOLA(improved) algorithm.
    
    Parameters:
    -----------
    input_audio : np.ndarray [shape=(channels, frames) or (frames,)]
        input audio data, must be float32, can be mono or multi-channel
    tempo : float
        Tempo scaling factor (1.0 = original tempo, 2.0 = double tempo, 0.5 = half tempo)
    sample_rate : int
        Sample rate of the audio
    sequence_ms : int 
        Processing sequence length in milliseconds
    seekwindow_ms : int
        Window length for seeking best overlap position in milliseconds
    overlap_ms : int
        Overlap length in milliseconds
    
    Returns:
    --------
    np.ndarray
        Time stretched audio data with same number of channels as input
    """
    
    input_audio = np.asarray(input_audio, dtype=np.float32)
    if input_audio.ndim == 1:
        input_audio = input_audio[np.newaxis, :]
    
    cdef:
        int channels = input_audio.shape[0]
        int frames = input_audio.shape[1]
        int overlap_length = (sample_rate * overlap_ms) // 1000
        int sequence_length = (sample_rate * sequence_ms) // 1000
        int seekwindow_length = (sample_rate * seekwindow_ms) // 1000
        float nominal_skip = tempo * (sequence_length - overlap_length)
        int output_frames = int(frames / tempo) + sequence_length * 2
        int skip = int(nominal_skip + 0.5)
        float skip_fract = 0.0
        int input_pos = 0
        int output_pos = 0
        int best_offset
        double corr, best_corr
        int i, ch, copy_length
        float scale1, scale2
        float[:] signal1_view
        float[:] signal2_view
        
        np.ndarray[np.float32_t, ndim=2] input_transposed
        np.ndarray[np.float32_t, ndim=2] output_buffer = np.zeros((channels, output_frames), dtype=np.float32)
        np.ndarray[np.float32_t, ndim=2] mid_buffer = np.zeros((channels, overlap_length), dtype=np.float32)
        
        
    while input_pos + seekwindow_length < frames:
        best_offset = 0
        best_corr = -1.0
        
        # cross correlation
        for i in range(seekwindow_length - overlap_length):
            signal1_view = input_audio[0, input_pos + i:input_pos + i + overlap_length]
            signal2_view = mid_buffer[0, :overlap_length]
            corr = calc_correlation(signal1_view, signal2_view)
            if corr > best_corr:
                best_corr = corr
                best_offset = i
        
        # overlap-add
        for ch in range(channels):
            for i in range(overlap_length):
                scale1 = float(i) / overlap_length
                scale2 = 1.0 - scale1
                output_buffer[ch, output_pos + i] = (
                    input_audio[ch, input_pos + best_offset + i] * scale1 + 
                    mid_buffer[ch, i] * scale2
                )
        sequence_offset = input_pos + best_offset + overlap_length
        sequence_length_current = min(sequence_length - overlap_length, 
                                   frames - sequence_offset)
        
        if sequence_length_current > 0:
            for ch in range(channels):
                output_buffer[ch, output_pos + overlap_length:
                            output_pos + overlap_length + sequence_length_current] = \
                    input_audio[ch, sequence_offset:
                              sequence_offset + sequence_length_current]
        
        if sequence_offset + sequence_length_current - overlap_length < frames:
            for ch in range(channels):
                mid_buffer[ch, :] = input_audio[ch,
                    sequence_offset + sequence_length_current - overlap_length:
                    sequence_offset + sequence_length_current]
        
        skip_fract += nominal_skip
        skip = int(skip_fract)
        skip_fract -= skip
        input_pos += skip
        output_pos += sequence_length_current
    
    result = output_buffer[:, :output_pos]
    if input_audio.shape[0] == 1:
        result = result[0]
        
    return result

@cython.boundscheck(False)
@cython.wraparound(False)
cdef double calc_correlation(float[:] signal1, float[:] signal2) nogil:
    """Calculate normalized cross-correlation between two signals"""
    cdef:
        int length = signal1.shape[0]
        int i
        double corr = 0.0
        double norm1 = 0.0
        double norm2 = 0.0
        
    for i in range(length):
        corr += signal1[i] * signal2[i]
        norm1 += signal1[i] * signal1[i]
        norm2 += signal2[i] * signal2[i]
        
    if norm1 == 0.0 or norm2 == 0.0:
        return 0.0
        
    return corr / sqrt(norm1 * norm2)
