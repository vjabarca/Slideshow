# import argparse
# from pathlib import Path
import pyyaml
import subprocess
import os
# from concurrent.futures import ProcessPoolExecutor, as_completed
# import hashlib
# import numpy as np
# import psutil
# from functools import reduce
import shutil
import time
import sys


######### Backup all files to external drive #########
def backup_add(source, files_list, destination_path):
    for item in files_list:
        source_path = os.path.join(source, item)
        dest_path = os.path.join(destination_path, item)
        if not os.path.exists(dest_path):
            shutil.copy(source_path, destination_path)
    return 1


def backup_delete(source , files_list, destination_path):
    for item in files_list:
        source_path = os.path.join(source, item)
        dest_path = os.path.join(destination_path, item)
        if not os.path.exists(dest_path):
            os.remove(source_path)
    return 1


######### Setup #########
def load_config():
    with open(resource_path("config_slideshow.yml")) as f:
        return yaml.safe_load(f)

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller .exe"""
    try:
        base_path = sys._MEIPASS  # PyInstaller creates a temp folder and stores path here
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


######### Main #########
def main():
    config_data = load_config()

    print(f"\nRemoving junk files {config_data['directories']['source']}")
    start_time = time.time()
    for junk_file in config_data['files']['junk_files']:
        subprocess.run(["find", config_data['directories']['source'], "-name", junk_file, "-delete"])
    end_time = time.time()
    elapsed_time = (end_time - start_time) / 60
    print(f"Done: {elapsed_time:.2f} minutes")

    print(f"\nRemoving ._ files from {config_data['directories']['source']}")
    start_time = time.time()
    subprocess.run(["find", config_data['directories']['source'], "-name", "._*", "-delete"])
    end_time = time.time()
    elapsed_time = (end_time - start_time) / 60
    print(f"Done: {elapsed_time:.2f} minutes")


    print(f"\nGetting list of files in source and destination directories")
    start_time = time.time()
    files_list_source = os.listdir(config_data['directories']['source'])
    files_list_destination = os.listdir(config_data['directories']['destination']) 
    end_time = time.time()
    elapsed_time = (end_time - start_time) / 60
    print(f"Done: {elapsed_time:.2f} minutes")


    print("\nBacking up updated directory")
    print(f"Source: {config_data['directories']['source']}")
    print(f"Destination: {config_data['directories']['destination']}")
    start_time = time.time()
    backup_add(config_data['directories']['source'], files_list_source, config_data['directories']['destination'])
    end_time = time.time()
    elapsed_time = (end_time - start_time) / 60
    print(f"Done: {elapsed_time:.2f} minutes")


    if len(files_list_destination) > 0:
        print(f"\nDeleting old files from {config_data['directories']['destination']} drive")
        start_time = time.time()
        backup_delete(config_data['directories']['destination'], files_list_destination, config_data['directories']['source'])
        end_time = time.time()
        elapsed_time = (end_time - start_time) / 60
        print(f"Done: {elapsed_time:.2f} minutes")
    input("Done!!")
if __name__ == '__main__':
    main()
