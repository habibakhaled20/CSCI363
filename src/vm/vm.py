# src/vm/vm.py
# vm_manager.py
# vm_manager.py  (FINAL WINDOWS VERSION - NO KVM ERROR)
# vm.py  (or vm_manager.py - complete VM creation module)
import subprocess
import json
import os

def run_command(cmd):
    """Run a shell command and return output or error message."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"

def create_vm():
    """Feature 1: Create and launch a Virtual Machine (interactive or from JSON config)."""
    print("\n" + "="*60)
    print("          CREATE VIRTUAL MACHINE")
    print("="*60)
    print("1. Interactive Mode")
    print("2. From JSON Configuration File")
    mode = input("\nChoose (1 or 2): ").strip()

    # Default values
    name = "ubuntu_vm"
    cpu = "2"
    ram = "2048"
    disk_size = "20"
    disk_file = "ubuntu_vm.qcow2"
    iso_path = None

    if mode == "1":
        # Interactive input
        name = input(f"VM Name [{name}]: ").strip() or name
        cpu = input(f"CPU cores [{cpu}]: ").strip() or cpu
        ram = input(f"RAM in MB [{ram}]: ").strip() or ram
        disk_size = input(f"Disk size in GB [{disk_size}]: ").strip() or disk_size
        iso_input = input("Path to ISO file (optional, press Enter to skip): ").strip().strip('"')
        if iso_input and os.path.exists(iso_input):
            iso_path = iso_input
        else:
            print("No valid ISO provided – will boot from disk only.")
        disk_file = f"{name}.qcow2"

    elif mode == "2":
        # Load from JSON config file
        config_path = input("Path to JSON config [example_config.json]: ").strip() or "example_config.json"
        if not os.path.exists(config_path):
            print("Error: Configuration file not found!")
            return
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
            name = config.get("name", name)
            cpu = str(config.get("cpu", cpu))
            ram = str(config.get("ram", ram))
            disk_size = str(config.get("disk", disk_size))
            iso_path = config.get("iso")
            disk_file = config.get("disk_name", f"{name}.qcow2")

            if iso_path and not os.path.exists(iso_path):
                print(f"Warning: ISO not found at '{iso_path}'. Continuing without bootable media.")
                iso_path = None
        except Exception as e:
            print(f"Error reading JSON file: {e}")
            return
    else:
        print("Invalid choice.")
        return

    # Create disk image if it doesn't exist
    if not os.path.exists(disk_file):
        print(f"\nCreating disk image: {disk_file} ({disk_size}GB)...")
        print(run_command(["qemu-img", "create", "-f", "qcow2", disk_file, f"{disk_size}G"]))
    else:
        print(f"Reusing existing disk: {disk_file}")

    # Windows-compatible QEMU command (no KVM, reliable graphics)
    cmd = [
        "qemu-system-x86_64",
        "-cpu", "Nehalem",              # Safe CPU model - avoids "host requires KVM" error
        "-smp", cpu,
        "-m", ram,
        "-drive", f"file={disk_file},format=qcow2",
        "-netdev", "user,id=net0",
        "-device", "virtio-net-pci,netdev=net0",
        "-vga", "std",                  # Standard VGA - most reliable for showing boot screen on Windows
        "-display", "sdl"               # Opens visible window
    ]

    if iso_path:
        cmd += ["-cdrom", iso_path, "-boot", "order=d"]
        print(f"Booting from ISO: {iso_path}")
    else:
        cmd += ["-boot", "order=c"]

    print(f"\nLaunching VM '{name}'... Close the QEMU window to return to menu.")
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\nVM terminated by user.")
    except Exception as e:
        print(f"Failed to launch QEMU: {e}")
        print("Tip: Ensure QEMU is installed and added to your PATH.")

    print("VM closed. Back to main menu.\n")

# For direct testing (optional)
if __name__ == "__main__":
    create_vm()