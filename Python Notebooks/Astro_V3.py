# -*- coding: utf-8 -*-
"""
Created on Sun Jan 25 15:52:40 2026

@author: MIR
"""

import numpy as np
from astropy.io import fits
from astropy.stats import mad_std
from scipy.ndimage import laplace

def detect_visual_noise(file_path):
    with fits.open(file_path) as hdul:
        # Using a higher percentile to avoid being fooled by 'black' pixels
        data = hdul[0].data.astype(float)
    
    # 1. Laplacian High-Pass Filter: Isolates pixel-to-pixel variations (the 'grain')
    # Clean images are smooth; noisy images have high local variance.
    edge_data = laplace(data)
    
    # 2. Use MAD (Median Absolute Deviation) instead of standard deviation
    # This is more robust against bright stars/galaxies
    noise_level = mad_std(edge_data)
    
    # 3. Calculate Signal-to-Noise Ratio (SNR)
    # We estimate 'Signal' as the 95th percentile of the data
    signal_level = np.percentile(data, 95) - np.median(data)
    snr = signal_level / noise_level if noise_level > 0 else 0
    
    print(f"--- Noise Analysis for {file_path} ---")
    print(f"Grain/Noise Intensity (MAD): {noise_level:.4f}")
    print(f"Estimated SNR: {snr:.2f}")

    # Interpret Results
    if snr < 5:
        print("Status: VERY NOISY (Signal is buried in grain)")
    elif snr < 15:
        print("Status: MODERATE NOISE")
    else:
        print("Status: CLEAN")

# Example usage
detect_visual_noise("E:/PortableGit/vla-set-1/vla_first_fits_1/J065857.0+642302.fits")
