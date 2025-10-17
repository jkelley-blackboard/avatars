import os
import csv
from shutil import copyfile, rmtree
import zipfile

# Configuration
data_file = 'list.csv'         # "|" delimited file: PK1 | image_id
image_dir = ''                 # Path to image source
ext = ".jpg"
batch_size = 100
sample_image = 'sample.jpg'    # Placeholder image

# Initialize counters
count = 0
batch = 0

# Create initial zip file
avatars_zip = zipfile.ZipFile("avatars.zip", "w", zipfile.ZIP_DEFLATED)

with open(data_file, newline='', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file, delimiter='|')
    for row in reader:
        count += 1
        pk1 = row[0]
        image_id = row[1]
        dirname = f"user{pk1}"
        filename = f"{image_id}{ext}"
        dst = os.path.join(dirname, filename)

        print(f"Adding: {dst} to avatars_{batch + 1}.zip")

        os.makedirs(dirname, exist_ok=True)

        # Use sample image as placeholder
        src = os.path.join(image_dir, sample_image)
        copyfile(src, dst)

        avatars_zip.write(dst, arcname=dst)

        rmtree(dirname)

        if count == batch_size:
            count = 0
            batch += 1
            avatars_zip.close()
            os.rename("avatars.zip", f"avatars_{batch}.zip")
            avatars_zip = zipfile.ZipFile("avatars.zip", "w", zipfile.ZIP_DEFLATED)

# Final batch
batch += 1
avatars_zip.close()
os.rename("avatars.zip", f"avatars_{batch}.zip")