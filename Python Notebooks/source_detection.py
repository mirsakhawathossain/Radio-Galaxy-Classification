"""
Source detection and masking tool for the FIRST survey.
"""
import os
from pathlib import Path

import bdsf
import numpy as np
from tools.data import clear_folder, fits_to_png, mask_single_image


def detect_and_mask(
    filename: str,
    frequency: float,
    beam: tuple,
    dilation: int,
    threshold_pixel: float = 5.0,
    threshold_island: float = 3.0,
    output_folder: str = "outputs",
):
    """
    Detect sources in a FITS file and mask out the sources from the noise map.

    Arguments:
        filename {str}: Path to the FITS file
        frequency {float}: Frequency of the observation
        beam {tuple}: Beam size of the observation
        dilation {int}: Dilation factor for the mask
        threshold_pixel {float}: Threshold for the pixel detection
        threshold_island {float}: Threshold for the island detection
        output_folder {str}: Folder to save the mask to
    """

    output_folder = os.path.join(output_folder, Path(filename).stem)
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    Path(os.path.join(output_folder, "masks")).mkdir(
        parents=True, exist_ok=True)
    Path(os.path.join(output_folder, "masked")).mkdir(
        parents=True, exist_ok=True)

    out_filename = (
        str(dilation) + "_" + str(threshold_island) +
        "_" + str(threshold_pixel)
    )
    mask_file = os.path.join(output_folder, "masks", out_filename + ".fits")
    masked_image_path = os.path.join(
        output_folder, "masked", out_filename + ".png")

    try:
        img = bdsf.process_image(
            filename,
            beam=beam,
            thresh_pix=threshold_pixel,
            thresh_isl=threshold_island,
            frequency=frequency,
        )

        img.export_image(
            img_type="island_mask",
            outfile=mask_file,
            mask_dilation=dilation,
        )

        mask_png = fits_to_png(mask_file)
        image_png = fits_to_png(filename)

        if mask_png is not None and image_png is not None:
            masked_image = mask_single_image(image_png, mask_png)
            masked_image.save(masked_image_path)

    except Exception as exception:  # pylint: disable=broad-except
        print(exception)


def grid_search(filename: str):
    """
    Grid search for the best parameters for the source detection.

    Arguments:
        filename {str}: Path to the FITS file
    """

    threshold_pixel = np.array(
        [2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.2, 4.4, 4.6, 4.8, 5.0]
    )
    threshold_island = np.array(
        [1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0])
    dilation = np.array([0, 1, 2, 3])
    frequency = 1.4e9
    beam = (0.0005, 0.0005, 0.0)

    for i in threshold_pixel:
        for j in threshold_island:
            for k in dilation:
                detect_and_mask(
                    filename,
                    frequency,
                    beam,
                    dilation=k,
                    threshold_pixel=i,
                    threshold_island=j,
                )


if __name__ == "__main__":
    clear_folder("bad", [".fits"])

    files = [
        os.path.join("bad", file)
        for file in os.listdir("bad")
        if file.endswith(".fits")
    ]

    for file in files:
        grid_search(file)

        with open("done.csv", "a", encoding="utf-8") as csv_file:
            csv_file.write(file)
