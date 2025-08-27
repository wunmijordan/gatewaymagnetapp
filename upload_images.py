import os
import csv
import cloudinary
from cloudinary.uploader import upload as cloudinary_upload

# Configure your Cloudinary credentials
cloudinary.config(
    cloud_name='dahx6bbyr',
    api_key='965118234472911',
    api_secret='EtuLzVQT9ngLvtxgh8uYoyMBelE'
)

# Folder containing your guest images
folder_path = "/mnt/c/Users/chinn/Pictures/GatewayMagnetCloudinaryUploads"

# CSV file to write
csv_file_path = "/mnt/c/Users/chinn/Pictures/GatewayMagnetCloudinaryUploads.csv"

# Dictionary to store results
uploaded_images = []

for filename in os.listdir(folder_path):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        file_path = os.path.join(folder_path, filename)
        try:
            response = cloudinary_upload(file_path, folder="guests")
            uploaded_images.append({
                "filename": filename,
                "cloudinary_url": response.get("secure_url"),
                "public_id": response.get("public_id")
            })
            print(f"Uploaded {filename} -> {response.get('secure_url')}")
        except Exception as e:
            print(f"Failed to upload {filename}: {e}")

# Write CSV
with open(csv_file_path, "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["filename", "cloudinary_url", "public_id"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for item in uploaded_images:
        writer.writerow(item)

print(f"\nCSV saved to {csv_file_path}")
