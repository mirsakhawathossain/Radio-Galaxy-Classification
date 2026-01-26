# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 10:40:35 2026

@author: MIR
"""

"""
Grid-search–based source detection and mask generation for FITS images.
"""

import os
from pathlib import Path
import itertools

import numpy as np
import bdsf
from astropy.io import fits

from data_tools import fits_to_png, mask_single_image


# -------------------------------
# Core source detection function
# -------------------------------
def detect_source_and_create_mask(
    fits_file: str,
    output_dir: str,
    frequency: float,
    beam: tuple,
    thresh_pix: float,
    thresh_isl: float,
    dilation: int,
    export_png: bool = True,
):
    """
    Run PyBDSF source detection and export mask FITS (and optional PNG).

    Returns
    -------
    mask_path : str
        Path to the generated mask FITS file
    """

    stem = Path(fits_file).stem
    param_tag = f"tp{thresh_pix}_ti{thresh_isl}_d{dilation}"

    mask_dir = Path(output_dir) / stem / "masks"
    masked_png_dir = Path(output_dir) / stem / "masked_png"

    mask_dir.mkdir(parents=True, exist_ok=True)
    masked_png_dir.mkdir(parents=True, exist_ok=True)

    mask_fits_path = mask_dir / f"{stem}_{param_tag}.fits"
    masked_png_path = masked_png_dir / f"{stem}_{param_tag}.png"

    try:
        img = bdsf.process_image(
            fits_file,
            frequency=frequency,
            beam=beam,
            thresh_pix=thresh_pix,
            thresh_isl=thresh_isl,
        )

        img.export_image(
            img_type="island_mask",
            outfile=str(mask_fits_path),
            mask_dilation=dilation,
        )

        if export_png:
            mask_png = fits_to_png(str(mask_fits_path))
            image_png = fits_to_png(fits_file)

            if mask_png is not None and image_png is not None:
                masked_image = mask_single_image(image_png, mask_png)
                masked_image.save(masked_png_path)

        return str(mask_fits_path)

    except Exception as exc:  # pylint: disable=broad-except
        print(f"[ERROR] {fits_file} | {param_tag} | {exc}")
        return None


# -------------------------------
# Grid search wrapper
# -------------------------------
def grid_search_source_detection(
    fits_file: str,
    output_dir: str,
    frequency: float,
    beam: tuple,
    threshold_pixel_grid: np.ndarray,
    threshold_island_grid: np.ndarray,
    dilation_grid: np.ndarray,
):
    """
    Perform grid search for a single FITS file.
    """

    for tp, ti, d in itertools.product(
        threshold_pixel_grid,
        threshold_island_grid,
        dilation_grid,
    ):
        detect_source_and_create_mask(
            fits_file=fits_file,
            output_dir=output_dir,
            frequency=frequency,
            beam=beam,
            thresh_pix=tp,
            thresh_isl=ti,
            dilation=d,
        )


# -------------------------------
# Folder-level batch processing
# -------------------------------
def process_fits_folder(
    input_fits_dir: str,
    output_dir: str,
):
    """
    Read all FITS files from a folder and run grid search on each.
    """

    input_fits_dir = Path(input_fits_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    fits_files = sorted(input_fits_dir.glob("*.fits"))

    if not fits_files:
        raise RuntimeError("No FITS files found in input directory.")

    # ---- Grid definition ----
    threshold_pixel = np.array(
        [2.8, 3.2, 3.6, 4.0, 4.4, 4.8, 5.0]
    )
    threshold_island = np.array(
        [1.0, 1.5, 2.0, 2.5, 3.0]
    )
    dilation = np.array([0, 1, 2, 3])

    # FIRST survey defaults
    frequency = 1.4e9
    beam = (0.0005, 0.0005, 0.0)

    for fits_file in fits_files:
        print(f"[INFO] Processing {fits_file.name}")
        grid_search_source_detection(
            fits_file=str(fits_file),
            output_dir=str(output_dir),
            frequency=frequency,
            beam=beam,
            threshold_pixel_grid=threshold_pixel,
            threshold_island_grid=threshold_island,
            dilation_grid=dilation,
        )


# -------------------------------
# CLI entry point
# -------------------------------
if __name__ == "__main__":
    INPUT_FITS_FOLDER = "E:/Documents/RGC Project/Data/Input_Folder"
    OUTPUT_MASK_FOLDER = "E:/Documents/RGC Project/Data/Mask_Folder"

    process_fits_folder(
        input_fits_dir=INPUT_FITS_FOLDER,
        output_dir=OUTPUT_MASK_FOLDER,
    )
