import os
import pydicom
from pydicom.uid import ExplicitVRLittleEndian, ImplicitVRLittleEndian
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
    "1.2.840.10008.1.2.5": "RLE Lossless"
}

def check_and_save_decompressed(dicom_file_path, output_folder):
    try:
        dp = pydicom.dcmread(dicom_file_path)
    except Exception as e:
        print(f"Error reading DICOM file: {e}")
        return

    ts_uid = dp.file_meta.TransferSyntaxUID
    print(f"\nTransfer Syntax UID: {ts_uid}")

    if ts_uid.name in [ExplicitVRLittleEndian.name, ImplicitVRLittleEndian.name]:
        print("This DICOM file is **not compressed**. No need to decompress.")
    elif str(ts_uid) in COMPRESSED_SYNTAXES:
        print(f"This DICOM file is **compressed** using: {COMPRESSED_SYNTAXES[str(ts_uid)]}")

        try:
            # Trigger decompression by accessing pixel_array
            pixel_array = dp.pixel_array
            print("Successfully decompressed the DICOM image.")

            # Change TransferSyntaxUID to uncompressed (Explicit VR Little Endian)
            dp.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

            # Update PixelData tag to uncompressed pixel data
            dp.PixelData = pixel_array.tobytes()

            # Create output folder if doesn't exist
            os.makedirs(output_folder, exist_ok=True)

            # Save decompressed file with same filename in output folder
            filename = os.path.basename(dicom_file_path)
            save_path = os.path.join(output_folder, filename)
            dp.save_as(save_path)
            print(f"Decompressed DICOM saved to: {save_path}")

            # Display the decompressed image
            display_image(pixel_array, dp)

        except Exception as e:
            print(f"Decompression or save failed: {e}")
    else:
        print("Unknown Transfer Syntax UID. It may be compressed with an unsupported method.")

def display_image(pixel_array, ds):
    """
    Display the DICOM image based on its photometric interpretation.
    """
    photometric_interpretation = ds.PhotometricInterpretation

    if photometric_interpretation == "MONOCHROME1" or photometric_interpretation == "MONOCHROME2":
        plt.imshow(pixel_array, cmap="gray")
    elif photometric_interpretation == "RGB":
        plt.imshow(pixel_array)
    else:
        print(f"Unsupported Photometric Interpretation: {photometric_interpretation}")
        return

    plt.gcf().canvas.manager.set_window_title('DICOM Viewer - Decompressed Image')
    plt.show()


if __name__ == "__main__":
    dicom_file = "./compressed_dicom/CT-JPEGLosslessSV1.dcm"  # can
    # dicom_file = "./compressed_dicom/YBR_FULL-RLE.dcm"  # cannot yet
    output_folder = "./decompressed_dicom"
    check_and_save_decompressed(dicom_file, output_folder)
