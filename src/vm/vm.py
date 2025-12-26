import subprocess
import json
import os

def create_vm_interactive():
    print("\n===== Create VM (Interactive Mode) =====")

    name = input("Enter VM name: ")
    cpu = input("Number of CPUs: ")
    ram = input("RAM (MB): ")
    disk = input("Disk size (GB): ")
    iso_path = input("Path to ISO file: ")

    # Validate input
    if not os.path.exists(iso_path):
        print("Error: ISO file not found.")
        return

    disk_file = f"{name}.qcow2"

    # Create disk
    print("\nCreating virtual disk...")
    subprocess.run(["qemu-img", "create", "-f", "qcow2", disk_file, f"{disk}G"])

    # Run VM
    print("\nStarting VM...")
    subprocess.run([
        "qemu-system-x86_64",
        "-name", name,
        "-m", ram,
        "-smp", cpu,
        "-drive", f"file={disk_file},format=qcow2",
        "-cdrom", iso_path,
        "-boot", "d"
    ])

if __name__ == "__main__":
    create_vm_interactive()
