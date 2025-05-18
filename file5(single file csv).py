import csv
import pydicom as dicom

# Load the DICOM file
ds = dicom.dcmread("./img/D0001.dcm")

# Write metadata to CSV
with open('my.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow("Group Elem Description VR Value".split())

    for elem in ds:
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
