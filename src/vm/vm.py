import subprocess
import os

def launch_vm_logic(name, cpu, ram, disk, iso):
    disk_file = f"{name}.qcow2"
    if not os.path.exists(disk_file):
        subprocess.run(["qemu-img", "create", "-f", "qcow2", disk_file, f"{disk}G"])
    
    cmd = [
        "qemu-system-x86_64", "-cpu", "Nehalem", "-smp", str(cpu), "-m", str(ram),
        "-drive", f"file={disk_file},format=qcow2", "-vga", "std", "-display", "sdl"
    ]
    if iso:
        cmd += ["-cdrom", iso.replace("\\", "/"), "-boot", "order=d"]
    
    subprocess.Popen(cmd) # Background process
    return f"VM '{name}' launched successfully."