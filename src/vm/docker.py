# src/vm/docker_manager.py
# docker.py - FINAL FIXED VERSION
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
    output = subprocess.run("docker images", shell=True, capture_output=True, text=True)
    print(output.stdout)
    if output.stderr:
        print("Error:", output.stderr)
    print("")

    
def list_running_containers():
    print("\n===== Running Containers =====")
    os.system("docker ps")

def stop_container():
    print("\n===== Stop Container =====")
    container = input("Enter container ID or name: ").strip()
    if container:
        os.system(f"docker stop {container}")
    else:
        print("No container specified.")

def search_local_image():
    print("\n===== Search Local Images =====")
    query = input("Enter search term: ").strip()
    if os.name == 'nt':
        os.system(f"docker images | findstr {query}")
    else:
        os.system(f"docker images | grep {query}")

def search_dockerhub():
    print("\n===== Search Docker Hub =====")
    query = input("Enter image name to search: ").strip()
    os.system(f"docker search {query}")

def pull_image():
    print("\n===== Pull Image =====")
    image = input("Enter image to pull (e.g., nginx:latest): ").strip()
    os.system(f"docker pull {image}")