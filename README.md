# Firmware Unpacker

This script can be used to unpack and than re-pack the firmware images for security testing purposes. 

# Usage

First run the binwalk command with following command `binwalk -t image.bin`.

This will give you the overview of the firmware image. Based on its output you should edit the variable `firmware_components` to perform extraction of the firmware.

The extraction itself can be done with following command:
`python3 FirmwareUnpacker.py unpack image.bin`

As a result a new folder with name `unpack_image.bin` will be created with extracted files.

After you are done with the changes, switch current working directory back to the location of the original image and run the following command:
`python3 FirmwareUnpacker.py pack image.bin`

You will be prompted if you want to skip the first section as that is likely to be image header which you may want to rebuild yourself. After the command is completed you will find a new image called `patched_image.bin` in your current working directory.

# Example

A sample `binwalk` output:
```
binwalk -t demo.bin                        

DECIMAL       HEXADECIMAL     DESCRIPTION
-------------------------------------------------------------------------------------------------------------------------------------------------
0             0x0             uImage header, header size: ...
64            0x40            LZMA compressed data, properties: 0x5D, dictionary size: 67108864 bytes, uncompressed size: -1 bytes
2097216       0x200040        Squashfs filesystem, little endian, version 4.0, compression:xz, size: ...
5570624       0x550040        Squashfs filesystem, little endian, version 4.0, compression:xz, size: ...
```

Example of `firmware_components` variable to match the above image:

```python
firmware_components = [
        {"name":"uimage","offset":0x0,"size":0x200040},
        {"name":"squashfs1","offset":0x200040,"size":0x550040-0x200040},
        {"name":"squashfs1","offset":0x550040,"size":0xA80000-0x550040}
    ]
```