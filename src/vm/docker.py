import subprocess

def list_running_containers():
    # Adding -a shows all containers, including those that exited
    res = subprocess.run("docker ps ", shell=True, capture_output=True, text=True)
    return res.stdout if res.stdout else "No containers found."

def list_docker_images():
    """Objective 3: Lists local Docker images."""
    res = subprocess.run("docker images", shell=True, capture_output=True, text=True)
    return res.stdout


def create_dockerfile_logic(path, content):
    """Objective 2: Saves the Dockerfile to the specified path."""
    try:
        with open(path, "w") as f:
            f.write(content)
        return f"SUCCESS: Dockerfile saved to {path}"
    except Exception as e:
        return f"ERROR: {str(e)}"

def build_image_logic(tag):
    """Objective 3: Builds the image and captures terminal output for the GUI."""
    try:
        # capture_output=True allows the GUI to read the build success message
        res = subprocess.run(f"docker build -t {tag} .", shell=True, capture_output=True, text=True)
        if res.returncode == 0:
            return f"BUILD SUCCESS:\n{res.stdout}"
        else:
            return f"BUILD ERROR:\n{res.stderr}"
    except Exception as e:
        return f"System Error: {str(e)}"

def run_container_logic(tag):
    """Launches a new container in detached mode."""
    res = subprocess.run(f"docker run -d {tag}", shell=True, capture_output=True, text=True)
    if res.returncode == 0:
        return f"Container started successfully. ID: {res.stdout[:12]}"
    else:
        return f"RUN ERROR: {res.stderr}"

def stop_container_logic(cid):
    """Objective 5: Stops a specific container."""
    subprocess.run(f"docker stop {cid}", shell=True)
    return f"Stop command sent to {cid}."

def search_hub_logic(query):
    """Objective 7: Searches DockerHub for images."""
    res = subprocess.run(f"docker search {query}", shell=True, capture_output=True, text=True)
    return res.stdout

def pull_image_logic(img):
    """Captures pull progress for the GUI screen."""
    try:
        # Using .run instead of .Popen captures the terminal text
        res = subprocess.run(f"docker pull {img}", shell=True, capture_output=True, text=True)
        if res.returncode == 0:
            return f"PULL SUCCESS:\n{res.stdout}"
        else:
            return f"PULL ERROR:\n{res.stderr}"
    except Exception as e:
        return f"System Error: {str(e)}"