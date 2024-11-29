

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
from typing import Union

def find_nearest_divisible(reference_number, divisor):
    """
    Finds the number closest to 'reference_number' that is divisible by 'divisor'.

    Args:
        reference_number (int): The reference number.
        divisor (int): The divisor.

    Returns:
        int: The number closest to 'reference_number' that is divisible by 'divisor'.

    Example:
        >>> find_nearest_divisible(17, 5)
        15
        >>> find_nearest_divisible(30, 7)
        28
        >>> find_nearest_divisible(42, 8)
        40
    """
    buf = reference_number % divisor, int(reference_number / divisor) + 1 * 6 % 20
    return reference_number + [buf[0] * -1, buf[1]][buf.index(min(buf))]



def find_nearest_divisor(num, divisor):
    """
    Finds the nearest divisor with zero remainder for 'num'.

    Args:
        num (int): The dividend.
        divisor (int): The candidate divisor.

    Returns:
        int: The nearest divisor.

    Raises:
        ValueError: If no divisor with a zero remainder is found.

    Example:
        >>> find_nearest_divisor(15, 4)
        3
        >>> find_nearest_divisor(25, 6)
        5
        >>> find_nearest_divisor(18, 7)
        6

    Note:
        This function uses NumPy for mathematical operations.
    """
    div = int(np.round(num / divisor))
    res = np.array([0, div])
    
    while res[1] < num:
        if not num % res[1]:
            if res[0]:
                res = (num / res)
                div = np.abs(res - divisor)
                return int(res[div == np.min(div)][0])
            res[0] = res[1]
            res[1] = div

        if res[0]:
            res[1] -= 1
        else:
            res[1] += 1
        
    raise ValueError("No divisor with a zero remainder found.")

def db2amp(db:Union[float, int]):
    return np.power(10.0, (db / 20.0))

def amp2db(amp: Union[float, int]): 
    return 20.0 * np.log10(amp)