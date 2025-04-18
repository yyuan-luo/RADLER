import math
import json
import numpy as np
import scipy.constants


def confmap2ra(name, radar_configs, radordeg='rad'):
    """
    Map confidence map to range(m) and angle(deg): not uniformed angle
    :param radar_configs: radar configurations
    :param name: 'range' for range mapping, 'angle' for angle mapping
    :param radordeg: choose from radius or degree for angle grid
    :return: mapping grids
    """
    Fs = radar_configs['sample_freq']
    sweepSlope = radar_configs['sweep_slope']
    num_crop_near = radar_configs['crop_num_near']
    num_crop_rear = radar_configs['crop_num_rear']
    fft_Rang = radar_configs['ramap_rsize'] + num_crop_near + num_crop_rear
    fft_Ang = radar_configs['ramap_asize']
    c = scipy.constants.speed_of_light

    if name == 'range':
        freq_res = Fs / fft_Rang  # frequency resolution
        freq_grid = np.arange(fft_Rang) * freq_res  # a frequency grid spanning the range map size
        # convert frequency grid to range grid
        # (freq_grid / sweepSlope) * c = range
        # / 2: round trip
        rng_grid = freq_grid * c / sweepSlope / 2
        rng_grid = rng_grid[num_crop_near: fft_Rang - num_crop_rear]
        return rng_grid

    if name == 'angle':
        # for [-90, 90], w will be [-1, 1] sine of angles ranging from the minimum angel to maximum angle
        # the angle in the annotation is also between [-1, 1]
        w = np.linspace(math.sin(math.radians(radar_configs['ra_min'])),
                        math.sin(math.radians(radar_configs['ra_max'])),
                        radar_configs['ramap_asize'])
        if radordeg == 'deg':
            agl_grid = np.degrees(np.arcsin(w))  # radians to degrees
        elif radordeg == 'rad':
            agl_grid = np.arcsin(w)  # radians
        else:
            raise TypeError
        return agl_grid


def ra2idx(rng, agl, range_grid, angle_grid):
    """Mapping from absolute range (m) and azimuth (rad) to ra indices."""
    rng_id, _ = find_nearest(range_grid, rng)
    agl_id, _ = find_nearest(angle_grid, agl)
    return rng_id, agl_id


def find_nearest(array, value):
    """Find nearest value to 'value' in 'array'."""
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx, array[idx]
