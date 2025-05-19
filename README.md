# DICOM Viewer

> You can understand the components of this project better at [YouTube playlist](https://www.youtube.com/watch?v=hWwAFNmPZFQ&list=PLEJnINKHyZIDRbBzm9RaH4yEkTLjmPOZr)
> and the library used [mataplotlib](https://matplotlib.org/stable/users/explain/quick_start.html).
> [DICOM_Library](https://www.dicomlibrary.com/dicom/transfer-syntax)

# Introduction
This project reads a series of DICOM files from a specified directory, reconstructs a 3D volume from the 2D image slices, and visualizes axial, sagittal, and coronal views using Python. It leverages popular libraries such as `pydicom`, `numpy`, and `matplotlib` for DICOM handling, numerical computations, and plotting respectively.

---

## Features

- Reads all DICOM files from a folder
- Sorts slices based on their spatial position
- Constructs a 3D volumetric representation from 2D slices
- Calculates the correct aspect ratios for realistic visualization
- Displays axial, sagittal, and coronal views of the 3D volume

---

# Dependencies and Installation
----------------------------
To install the DICOM Viewer, please follow these steps:

1. Clone the repository to your local machine.

2. Install the required dependencies by running the following command:
   ```
   python -m pip install -r requirements.txt

   ```
