# src/vm/docker_manager.py
# docker.py - FINAL FIXED VERSION
# docker.py - FINAL FIXED VERSION (with reliable output capture)

import subprocess
import os

def run_command(cmd):
    """Run command and return stdout (even if error)"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.stdout:
            return result.stdout.strip()
        if result.stderr:
            return f"Error: {result.stderr.strip()}"
        return "Command executed (no output)"
    except Exception as e:
        return f"Exception: {str(e)}"

def create_dockerfile():
    print("\n===== Create Dockerfile =====")
    path = input("Enter path to save Dockerfile (e.g., Dockerfile): ").strip() or "Dockerfile"
    dir_name = os.path.dirname(path)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name)
        print(f"Created directory: {dir_name}")

    print("\nEnter Dockerfile contents (type 'END' on a new line when done):")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)

    try:
        with open(path, "w") as f:
            f.write("\n".join(lines) + "\n")
        print(f"\nDockerfile created successfully: {os.path.abspath(path)}")
    except Exception as e:
        print(f"Failed to write file: {e}")

def build_docker_image():
    print("\n===== Build Docker Image =====")
    dockerfile_path = input("Path to Dockerfile [Dockerfile]: ").strip() or "Dockerfile"
    
    if not os.path.exists(dockerfile_path):
        print(f"Error: Dockerfile not found at {dockerfile_path}")
        return
    
    name = input("Image name (e.g., myapp): ").strip()
    if not name:
        print("Image name required!")
        return
    tag = input("Tag [latest]: ").strip() or "latest"
    full_tag = f"{name}:{tag}"
    
    build_dir = os.path.dirname(dockerfile_path) or "."
    
    print(f"\nBuilding {full_tag} from {dockerfile_path}...")
    print(f"Using build context: {os.path.abspath(build_dir)}")
    
    cmd = f"docker build -f \"{dockerfile_path}\" -t {full_tag} \"{build_dir}\""
    output = run_command(cmd)
    print("\n" + output)
    
    if "Successfully tagged" in output or not output.startswith("Error"):
        print(f"\nSUCCESS! Image '{full_tag}' built.")
        print("Check with option 4 (List Docker Images)")
    else:
        print("\nBuild failed.")

def list_docker_images():
    print("\n===== Docker Images =====")
    output = run_command("docker images")
    print(output)

def list_running_containers():
    print("\n===== Running Containers =====")
    output = run_command("docker ps")
    print(output)

def stop_container():
    print("\n===== Stop Container =====")
    container = input("Enter container ID or name: ").strip()
    if container:
        output = run_command(f"docker stop {container}")
        print(output)
    else:
        print("No container specified.")

def search_local_image():
    print("\n===== Search Local Images =====")
    query = input("Enter search term: ").strip()
    if not query:
        print("No search term provided.")
        return
    # Use run_command to capture output reliably
    if os.name == 'nt':
        output = run_command(f"docker images | findstr {query}")
    else:
        output = run_command(f"docker images | grep {query}")
    print(output)

def search_dockerhub():
    print("\n===== Search Docker Hub =====")
    query = input("Enter image name to search: ").strip()
    if query:
        output = run_command(f"docker search {query}")
        print(output)
    else:
        print("No search term provided.")

def pull_image():
    print("\n===== Pull Image =====")
    image = input("Enter image to pull (e.g., nginx:latest): ").strip()
    if image:
        output = run_command(f"docker pull {image}")
        print(output)
    else:
        print("No image specified.")