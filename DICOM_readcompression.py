import pydicom
import matplotlib.pyplot as plt


# Dictionary of common compressed Transfer Syntax UIDs
COMPRESSED_SYNTAXES = {
    "1.2.840.10008.1.2.4.50": "JPEG Baseline (Process 1) - Lossy",
    "1.2.840.10008.1.2.4.57": "JPEG Lossless, Non-Hierarchical (Process 14)",
    "1.2.840.10008.1.2.4.70": "JPEG Lossless, Non-Hierarchical (Process 14 [Selection 1])",
    "1.2.840.10008.1.2.4.80": "JPEG-LS Lossless Image Compression",
    "1.2.840.10008.1.2.4.81": "JPEG-LS Lossy Image Compression",
    "1.2.840.10008.1.2.4.90": "JPEG 2000 Image Compression (Lossless Only)",
    "1.2.840.10008.1.2.4.91": "JPEG 2000 Image Compression",
    "1.2.840.10008.1.2.5": "RLE Lossless",
}

def check_compression(dicom_file_path):
    dp = pydicom.dcmread(dicom_file_path)

    # Get the Transfer Syntax UID
    ts_uid = dp.file_meta.TransferSyntaxUID
    print(f"\nTransfer Syntax UID: {ts_uid}")

    if ts_uid.name in ['Explicit VR Little Endian', 'Implicit VR Little Endian']:
        print("This DICOM file is **not compressed**.")
    elif str(ts_uid) in COMPRESSED_SYNTAXES:
        print(f"This DICOM file is **compressed** using: {COMPRESSED_SYNTAXES[str(ts_uid)]}")
        
        try:
            # Accessing pixel_array will trigger decompression
            pixel_array = dp.pixel_array
            print("Successfully decompressed the DICOM image.")

            # Display image
            plt.figure(figsize=(8, 8)).canvas.manager.set_window_title('DICOM Viewer - Decompressed Image')
            plt.imshow(pixel_array)
            plt.axis('off')
            plt.show()

        except Exception as e:
            print(f"Decompression failed: {e}")
    else:
        print("Unknown Transfer Syntax UID. It may be compressed with an unsupported method.")


if __name__ == "__main__":
    dicom_file = "./compressed_dicom/YBR_FULL-RLE.dcm"
    check_compression(dicom_file)
