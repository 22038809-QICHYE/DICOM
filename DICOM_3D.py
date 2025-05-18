import pydicom
import numpy as np
import matplotlib.pyplot as plt
import os

def load_dicom_series(path):
    """Load and sort a series of DICOM slices from the given folder path."""
    files = [f for f in os.listdir(path) if f.lower().endswith(".dcm")]
    slices = [pydicom.dcmread(os.path.join(path, f), force=True) for f in files]
    slices.sort(key=lambda x: x.ImagePositionPatient[2])
    return slices

def build_volume(slices):
    """Convert sorted DICOM slices into a 3D volume."""
    img_shape = list(slices[0].pixel_array.shape)
    img_shape.append(len(slices))
    volume = np.zeros(img_shape)

    for i, s in enumerate(slices):
        volume[:, :, i] = s.pixel_array

    return volume

def compute_aspect_ratios(slices):
    """Compute aspect ratios for axial, sagittal, and coronal planes."""
    pixel_spacing = slices[0].PixelSpacing
    slice_thickness = slices[0].SliceThickness

    axial = pixel_spacing[1] / pixel_spacing[0]
    sagittal = pixel_spacing[1] / slice_thickness
    coronal = slice_thickness / pixel_spacing[0]

    return axial, sagittal, coronal

def show_views(volume, aspect_ratios):
    """Display axial, sagittal, and coronal views using matplotlib."""
    axial_ratio, sagittal_ratio, coronal_ratio = aspect_ratios
    shape = volume.shape

    plt.figure(figsize=(8, 8)).canvas.manager.set_window_title('DICOM Viewer - Axial, Sagittal, Coronal Views')
    #plt.suptitle("DICOM Viewer", fontsize=16) 

    # Axial View (looking from top down on the body, like lying in a scanner)
    axial = plt.subplot(2, 2, 1)
    plt.title("Axial")
    plt.imshow(volume[:, :, shape[2] // 2])
    axial.set_aspect(axial_ratio)

    # Sagittal view (side view: left to right through the head or body)
    sagittal = plt.subplot(2, 2, 2)
    plt.title("Sagittal")
    plt.imshow(volume[:, shape[1] // 2, :])
    sagittal.set_aspect(sagittal_ratio)

    # Coronal view (front-facing view: like looking directly at the patient)
    coronal = plt.subplot(2, 2, 3)
    plt.title("Coronal")
    plt.imshow(volume[shape[0] // 2, :, :].T)
    coronal.set_aspect(coronal_ratio)

    plt.tight_layout()
    plt.show()

def main():
    dicom_path = "./img"

    slices = load_dicom_series(dicom_path)
    volume = build_volume(slices)
    aspect_ratios = compute_aspect_ratios(slices)
    
    print("Volume shape:", volume.shape)
    show_views(volume, aspect_ratios)


if __name__ == "__main__":
    main()
