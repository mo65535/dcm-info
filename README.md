dicom-info
==========

A small Python script for printing DICOM metadata info.

Useful for navigating folders of images reconstructed by the scanners, which tend to have uninformative names and a hierarchy like

```
4194_09152011/
|-- 001
|   |-- I0001.dcm
|   |-- I0002.dcm
|   |-- <...>
|   |-- I0014.dcm
|   `-- I0015.dcm
|-- 002
|   |-- I0001.dcm
|   `-- <...>
|-- 003
|   |-- I0001.dcm
|   `-- <...>
|-- 004
|   |-- I0001.dcm
|   `-- <...>
|-- 005
|   |-- I0001.dcm
|   `-- <...>
`-- 006
    |-- I0001.dcm
    `-- <...>
```    
    
    
Example usage
=============

By default it descends into subdirectories of the specified search path.
If you have several MR exams in a folder, e.g. for a project they are part of, you can point this script at the project folder and get info about all the exams in the subdirectories.

For speed, it only reads metadata from the first DICOM file it finds in each folder.
If you have a folder that contains a mix of multiple DICOM series (this is not ideal), the `--find-all-uniques` flag will force it to check all DICOM files (slower) and print the unique values that were encountered in the metadata.

Call the script with the `--help` argument for more info.
Here are some typical use cases.

```bash
cd /data/users/<USERNAME>/DICOMS_from_scanner/4194_09152011
dcm-info ./
```

**Output:**
```
./001:
  SeriesDescription:   3pl loc FGRE
./002:
  SeriesDescription:   FGRE
./003:
  SeriesDescription:   Ax T1 FLAIR
./004:
  SeriesDescription:   Sag T1 FLAIR
./005:
  SeriesDescription:   Cor T1 FLAIR
./006:
  SeriesDescription:   Cartesian bSSFP

```

Or, showing name, date, and time of day as well:
```
cd /data/<USERNAME>/DICOMS_from_scanner/4194_09152011
dcm-info -ndt ./
```
**Output:**
```
./001:
  SeriesDescription:   3pl loc FGRE
  PatientName:         Namesworth^Pat
  AcquisitionDate:     20110915
  AcquisitionTime:     203841
./002:
  SeriesDescription:   FGRE
  PatientName:         Namesworth^Pat
  AcquisitionDate:     20110915
  AcquisitionTime:     204107
./003:
  SeriesDescription:   Ax T1 FLAIR
  PatientName:         Namesworth^Pat
  AcquisitionDate:     20110915
  AcquisitionTime:     210221
./004:
  SeriesDescription:   Sag T1 FLAIR
  PatientName:         Namesworth^Pat
  AcquisitionDate:     20110915
  AcquisitionTime:     210938
./005:
  SeriesDescription:   Cor T1 FLAIR
  PatientName:         Namesworth^Pat
  AcquisitionDate:     20110915
  AcquisitionTime:     211441
./006:
  SeriesDescription:   Cartesian bSSFP
  PatientName:         Namesworth^Pat
  AcquisitionDate:     20110915
  AcquisitionTime:     212536
```


TODO
====

- [ ] Clean up some functions.
- [ ] Add options to read other elements of DICOM metadata.

       
