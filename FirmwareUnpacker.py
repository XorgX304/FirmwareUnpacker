import sys
import os

def main():
    # EDIT THIS!!!
    firmware_components = [
        {"name":"uimage","offset":0x0,"size":0x40},
        {"name":"uimage2","offset":0x40,"size":0x200040 - 0x40},
        {"name":"squashfs1","offset":0x200040,"size":0x550040-0x200040},
        {"name":"squashfs1","offset":0x550040,"size":0xA88040-0x550040}
    ]
    # Check corret usage of the script
    if len(sys.argv) != 3:
        print(f"[*] Usage: {argv[0]} <unpack|pack> <path_to_image>")
        print(f"\tFor unpacking use following syntax:\n\t{argv[0]} unpack firmware.img")
        print(f"\tThe above command will create folder with name \"unpack_firmware.img\" with contents of the firmware file.")
        print(f"\tTo pack the firmware back, first update the files within the \"unpack_firmware.img\" folder with desired changes and than run following command (from the same folder where you executed previous command):")
        print(f"\t{argv[0]} pack firmware.img")
        print(f"\tThis will create patched_firmware.img file with your changes (You have an option to skip the first part for cases where you want to rebuild the heder yourself).")
        return

    # Unpack
    if sys.argv[1] == "unpack":
        # Create directory for unpacking
        os.mkdir(f"unpack_{sys.argv[2]}")
        # Open the firmware image file
        with open(sys.argv[2],"rb") as firmware_image:
            # For each component
            for component in firmware_components:
                # Find the offset
                firmware_image.seek(component["offset"],0)
                # Read the data
                data = firmware_image.read(component["size"])
                # Write it to new file
                with open(f'unpack_{sys.argv[2]}/{component["name"]}',"wb") as output:
                    output.write(data)
                    print(f'[*] Wrote {component["name"]} ({hex(component["size"])} bytes)')
    
    # Pack
    elif sys.argv[1] == "pack":
        # Open destination file
        with open(f"patched_{sys.argv[2]}","wb") as output_file:
            yes = {'yes','y', 'ye', ''}
            no = {'no','n'}
            choice = input("[?] Skip the first component (Could be header)? ").lower()
            if choice in yes:
                firmware_components = firmware_components[1:]
            elif choice in no:
                pass
            else:
                sys.stdout.write("Please respond with 'yes' or 'no'")
            for component in firmware_components:
                with open(f"unpack_{sys.argv[2]}/"+component["name"],"rb") as file_input:
                    data = file_input.read()
                    output_file.write(data)
                    # Write data to file
                    padding = component["size"] - len(data)
                    # Add padding to original size
                    output_file.write(b"\x00" * padding)
                    print(f'[*] Wrote {component["name"]} ({hex(len(data))} bytes with {hex(padding)} bytes of padding. Total: {hex(component["size"])} bytes)')

if __name__ == '__main__':
    main()