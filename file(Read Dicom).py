import pydicom as dicom

path="./img/D0001.dcm"
x=dicom.dcmread(path)
print(dir(x))
print(x)