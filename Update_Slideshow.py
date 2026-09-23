import argparse
# from pathlib import Path
import yaml
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
def parse_config_data(config_yml):
    with open(config_yml, "r") as file:
        config_data = yaml.safe_load(file)
    return config_data

def parse_input():
    parser = argparse.ArgumentParser(
        description="This script will look for duplicate files inside directories and between all directories inside a pre-designated directory")
    parser.add_argument("-y", "--yml", help="Path for the configuration file", required=True, type=str, dest="yml_file")
    return parser.parse_args()

def get_asset_path_OLD(relative_path):
    """ Get absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_resource_path(relative_path):
    """ Get absolute path to the resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


######### Main #########
def main():
    # Use this function to load config file
    # config_path = get_asset_path("config_slideshow.yml")
    config_path = get_resource_path("config_slideshow.yml")
    # Parse user inputs
    args = parse_input()
    # Parse yml_file
    config_data = parse_config_data(args.yml_file)


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