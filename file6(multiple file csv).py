import pydicom as dicom
import os
import csv

data_dir = "./img"
patients = os.listdir(data_dir)

with open('file.csv', 'w', newline='', encoding='utf-8') as myfile:
    writer = csv.writer(myfile)
    writer.writerow(["Group", "Elem", "Description", "VR", "Value"])

    for patient in patients:
        if patient.lower().endswith('.dcm'):
            dm = dicom.dcmread(os.path.join(data_dir, patient))
            for elem in dm:
                if elem.VR == "SQ":
                    continue  # Skip sequences
                try:
                    value_str = str(elem.value)
                    if len(value_str) > 100:
                        value_str = value_str[:97] + "..."
                except Exception:
                    value_str = "<unreadable>"

                writer.writerow([
                    f"{elem.tag.group:04x}",
                    f"{elem.tag.element:04x}",
                    elem.name,
                    elem.VR,
                    value_str
                ])
