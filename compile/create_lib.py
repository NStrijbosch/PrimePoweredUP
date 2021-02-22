#!/usr/bin/python3
# this is for creating the remote library

import os

files = ["../src/imports.py", "../src/pu_remote.py", "../src/ble_handler.py", "../src/decoder.py", "../src/constants.py"]
data = [None] * len(files)
output = []


for i, name in enumerate(files):
    with open(name) as fp:
        data[i] = fp.readlines()
        for y, line in enumerate(data[i]):
            if line.strip('\n') == "# ERASE":
                data[i] = data[i][y + 1:]

for py in data:
    output = output + py

with open('remote.py', 'w') as fp:
    fp.writelines(output)

os.system("python3 -m mpy_cross ./remote.py")
os.system("rm -rf ./remote.py")

print("create library!")