
import numpy as np
cimport numpy as np


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



cpdef enum FadePreset:
    SMOOTH_ENDS
    BELL_CURVE
    KEEP_ATTACK_ONLY
    LINEAR_FADE_IN
    LINEAR_FADE_OUT
    PULSE
    REMOVE_ATTACK
    SMOOTH_ATTACK
    SMOOTH_FADE_IN
    SMOOTH_FADE_OUT
    SMOOTH_RELEASE
    TREMORS
    ZIGZAG_CUT

cpdef np.ndarray[double, ndim=1] generate_envelope(
    int envlen,
    FadePreset preset,
    bint enable_spline,
    double spline_sigma,
    double fade_max_db,
    double fade_min_db,
    double fade_attack,
    double fade_release,
    int buffer_size,
    double sawtooth_freq
)

cdef double db2amp(double db) nogil
