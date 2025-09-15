![GitHub License](https://img.shields.io/github/license/mirsakhawathossain/Radio-Galaxy-Classification)
![GitHub contributors](https://img.shields.io/github/contributors/mirsakhawathossain/Radio-Galaxy-Classification)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/mirsakhawathossain/Radio-Galaxy-Classification)
![GitHub Created At](https://img.shields.io/github/created-at/mirsakhawathossain/Radio-Galaxy-Classification)
[![nbviewer](https://img.shields.io/badge/render-nbviewer-orange.svg)](https://nbviewer.org/github/mirsakhawathossain/Radio-Galaxy-Classification/tree/main/)

# Radio Galaxy classification

The goal of this project is to develop a python package for classifying different morphological types of radio Active Galactic Nuclei (AGN) using artificial neural networks (ANN) and maintain the package through regular upgrades. The package is called RGC after Radha Gobinda Chandra (1878-1975), a Bangladeshi-Indian amateur astronomer who contributed more than fifty thousand observations to the American Association of Variable Star Observers (Maitra 2021) and reported the observation of Halley’s Comet in 1910 in Bangla (Kapoor 2023).

# Important Links
* [Cosmic ray removal](https://www.astropy.org/ccd-reduction-and-photometry-guide/v/dev/notebooks/08-03-Cosmic-ray-removal.html)
* [Background Estimation](https://photutils.readthedocs.io/en/latest/user_guide/background.html)
* [Complex 2D Background: Imaging Sky Background Estimation](https://eteq.github.io/notebooks-for-all/Imaging_Sky_Background_Estimation.html)
* [Construction of an artificial (but realistic)](https://www.astropy.org/ccd-reduction-and-photometry-guide/v/dev/notebooks/01-03-Construction-of-an-artificial-but-realistic-image.html)
* [Image Segmentation](https://photutils.readthedocs.io/en/latest/user_guide/segmentation.html)
* [Remove image background with 5 lines of python code (General Image)](https://penscola.medium.com/remove-image-background-with-5-lines-of-python-code-b3ca7beba869)

# Simple Background Remove Code
Removing the background in astronomical images using Astropy, particularly through its affiliated package photutils, involves estimating the background and then subtracting it from the data. Here's a common approach: Estimate Background Statistics with Sigma Clipping.
Use astropy.stats.sigma_clipped_stats to get robust estimates of the background mean, median, and standard deviation, excluding sources.

```python

from astropy.stats import sigma_clipped_stats
    import numpy as np

    # Assuming 'data' is your 2D astronomical image array
    mean, median, std = sigma_clipped_stats(data, sigma=3.0)
    print(f"Background Mean: {mean}, Median: {median}, Std Dev: {std}")
```
* Estimate Background and Background RMS using ```photutils.background```:
```
For more sophisticated background estimation, particularly with varying backgrounds, ```photutils.background``` provides tools like ```Background2D```.
```python
    from photutils.background import Background2D, MedianBackground, SExtractorBackground

    # Create a background estimator (e.g., MedianBackground)
    bkg_estimator = MedianBackground()

    # Create a background RMS estimator (e.g., SExtractorBackground)
    bkgrms_estimator = SExtractorBackground()

    # Estimate 2D background and background RMS
    bkg = Background2D(data, (50, 50), filter_size=(3, 3),
                       bkg_estimator=bkg_estimator, bkgrms_estimator=bkgrms_estimator)

    # Access the background and background RMS images
    background_image = bkg.background
    background_rms_image = bkg.background_rms
```
Subtract the Background.
Once you have an estimate of the background, subtract it from your original data.
```python
    background_subtracted_data = data - background_image
```
**Additional Considerations:**

**Masking Sources:**
For more accurate background estimation, especially in crowded fields, you can mask out detected sources before calculating background statistics. This often involves using ```photutils.segmentation``` to create a segmentation map of sources.
Custom Background Functions:
```photutils.background``` allows for custom background and background RMS estimators if the built-in options are not sufficient for your specific data.

**Cosmic Ray Removal:**
Before background subtraction, it is often beneficial to remove cosmic rays, which can be done using packages like ```ccdproc``` or ```Astro-SCRAPPY```. [Reference Google](https://www.google.com/search?q=how+to+remove+background+in+astropy&ie=UTF-8)
