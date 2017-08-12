#!/usr/bin/env python

import glob
import json
import os
import re
import sys
from os.path import isfile, join

private_dir = sys.argv[1]

def search_dir(directory):
    files_to_copy = []
    for item in os.listdir(directory):
        full_path = join(directory, item)
        if isfile(full_path):
            match = re.match('(.*)\.template(.*)', full_path)
            if match:
                new_file_path = ''.join(match.groups())
                files_to_copy.append({
                    'old_file_path': full_path,
                    'new_file_path': new_file_path,
                })
        else:
            # is a directory
            files_to_copy += search_dir(full_path)

    return files_to_copy

def copy_files(files_to_copy, force_overwriting):
    """
    `files_to_copy` should be an array of {'old_file_path': string, 'new_file_path': string}
    """
    for file_to_copy in files_to_copy:
        new_file_path = file_to_copy['new_file_path']
        if force_overwriting or not isfile(new_file_path):
            with open(file_to_copy['old_file_path'], 'r') as f:
                contents = f.read()
            with open(new_file_path, 'w') as f:
                f.seek(0)  # redundant but "good practice"
                f.write(contents)
                f.truncate()  # redundant but "good practice"

files_to_copy = search_dir(private_dir)
copy_files(files_to_copy, False)
