# PEMS_Dataset_Process

This repository is the script to make PEMS dataset just like PEMSD4/PEMSD8 used in https://github.com/guoshnBJTU/ASTGCN-r-pytorch.

## Prepare

`` 
pip install requests numpy retrying pandas
``

Use ``Python == 3.x``

## Download data from PEMS

Select the vds you want to use from PEMS, and save them in `%city_mainline.txt`.

Type your account, password and choose the time you need at `start_time, end_time` in `download_vds_data.py`.

Use `python download_vds_data.py` to download the original data of vds.

## Create PEMS dataset

Use `python create_traffic_npz.py` to merge the orginal data, then combine them to `.npz` dataset just like PEMSD4/PEMSD8.

## Create Accident dataset

Use `python create_incident_npz.py` to merge the accident data.

Before you run this code, you need download the accident data from the PEMS CHP Incident system, Just like PEMS_Dataset_Process/Tustin/22-01-01_22-01-07/incident/incident.xlsx.

## Combine  PEMS dataset with Accident data

Use `python create_PEMS_npz.py` to combine PEMS dataset with Accident data. Then you could get a PEMS dataset with accident.
