import numpy as np
from astropy.io import fits
from astropy.stats import sigma_clipped_stats
from photutils.background import Background2D, MedianBackground

def analyze_fits_noise(file_path):
    # Load the FITS image data
    with fits.open(file_path) as hdul:
        data = hdul[0].data  # Assuming image is in the primary HDU
    
    # Method 1: Simple Global Statistics (Quick)
    # sigma_clipped_stats ignores outliers like bright stars to find the 'true' background
    mean, median, std = sigma_clipped_stats(data, sigma=3.0)
    
    # Method 2: 2D Background Estimation (Detailed)
    # This accounts for noise that might vary across the image
    bkg_estimator = MedianBackground()
    bkg = Background2D(data, (50, 50), filter_size=(3, 3), 
                       bkg_estimator=bkg_estimator)
    
    # Calculate average background noise (RMS)
    avg_noise = bkg.background_rms_median
    
    print(f"File: {file_path}")
    print(f"Global Background Std Dev (Noise): {std:.4f}")
    print(f"2D Median Background RMS: {avg_noise:.4f}")
    
    # Threshold check: images with high std relative to signal are 'noisy'
    if avg_noise > 10.0:  # Threshold depends on your specific camera/sensor
        print("Status: HIGH NOISE DETECTED")
    else:
        print("Status: Clean image")

# Example usage
analyze_fits_noise("E:/Documents/RGC Project/Data/vla-set-1/Divided_Folders/Folder-3/J065419.3+635906.fits")
