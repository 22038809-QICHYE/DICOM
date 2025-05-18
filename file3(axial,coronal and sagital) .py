import pydicom as dicom
import numpy as np
import matplotlib.pyplot as plt
import os

path="./img"
ct_images=os.listdir(path)

slices = [dicom.dcmread(path + '/' + img, force=True) for img in ct_images]
#print(slices)

slices = sorted(slices,key=lambda x:x.ImagePositionPatient[2])

pixel_spacing = slices[0].PixelSpacing
slices_thickess = slices[0].SliceThickness

# To ensure each image is displayed with real-world proportions.
# axial view (looking from top down on the body, like lying in a scanner)
axial_aspect_ratio = pixel_spacing[1]/pixel_spacing[0]
# sagittal view (side view: left to right through the head or body)
sagital_aspect_ratio = pixel_spacing[1]/slices_thickess
# coronal view (front-facing view: like looking directly at the patient)
coronal_aspect_ratio = slices_thickess/pixel_spacing[0]

#print("Pixel spacing is:",pixel_spacing)
#print("Slices Thickness is:",slices_thickess)
#print("Axial Aspect Ratio:",axial_aspect_ratio)
#print("Sagital Aspect Ratio:",sagital_aspect_ratio)
#print("Coronal Aspect Ratio:",coronal_aspect_ratio)

#=============================================================================

img_shape = list(slices[0].pixel_array.shape)
img_shape.append(len(slices))
volume3d = np.zeros(img_shape)

for i,s in enumerate(slices):
    array2D=s.pixel_array
    volume3d[:,:,i]= array2D

axial=plt.subplot(2,2,1)
plt.title("Axial")
plt.imshow(volume3d[:,:,img_shape[2]//2])
axial.set_aspect(axial_aspect_ratio)

sagital=plt.subplot(2,2,2)
plt.title("Sagittal")
plt.imshow(volume3d[:,img_shape[1]//2,:])
sagital.set_aspect(sagital_aspect_ratio)

coronal = plt.subplot(2,2,3)
plt.title("Coronal")
plt.imshow(volume3d[img_shape[0]//2,:,:].T)
coronal.set_aspect(coronal_aspect_ratio)

plt.show()

print(array2D.shape)
print(volume3d.shape)    