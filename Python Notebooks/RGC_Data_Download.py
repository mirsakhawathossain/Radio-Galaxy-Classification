import pandas as pd
import os
from astropy.coordinates import SkyCoord
from astroquery.skyview import SkyView
from astropy.io import fits
from astropy import units as u
from tqdm import tqdm
import re

# Load the catalog
catalog = pd.read_csv("/home/ubuntu/catalog_first_VLA.csv")

# Output directory
output_dir = "/home/ubuntu/vla_first_fit/"
os.makedirs(output_dir, exist_ok=True)

# Survey name
survey = "VLA FIRST (1.4 GHz)"

# Function to clean FITS header
def clean_fits_header(hdu):
    try:
        header = hdu.header
        if 'COMMENT' in header:
            comments = header['COMMENT']
            if isinstance(comments, list):
                cleaned = [re.sub(r'[^\x20-\x7E]', ' ', str(c)) for c in comments]
            else:
                cleaned = [re.sub(r'[^\x20-\x7E]', ' ', str(comments))]
            del header['COMMENT']
            for c in cleaned:
                header.add_comment(c)
    except Exception as e:
        print("[WARN] Failed to sanitize header:", e)

# Iterate over each row and download FITS
for idx, row in tqdm(catalog.iterrows(), total=len(catalog)):
    try:
        # RA/DEC
        ra = row["RAJ2000"]
        dec = row["DEJ2000"]

        # Filename using 'First' column
        tag = str(row["FIRST"]).strip()
        filename = os.path.join(output_dir, f"{tag}.fits")

        # Skip if already downloaded
        if os.path.exists(filename):
            continue

        # Convert to SkyCoord
        coord = SkyCoord(ra=ra, dec=dec, unit=(u.hourangle, u.deg))

        # Query SkyView
        images = SkyView.get_images(position=coord, survey=[survey], coordinates="J2000", pixels=(300, 300))

        # Save FITS
        if images:
            hdulist = images[0]
            clean_fits_header(hdulist[0])
            hdulist.writeto(filename, overwrite=True, output_verify='ignore')
        else:
            print(f"No image returned for index {idx}")

    except Exception as e:
        print(f"[ERROR] Index {idx} - RA: {ra}, DEC: {dec} => {e}")
