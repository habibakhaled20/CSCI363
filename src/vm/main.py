# src/vm/main.py
# main.py - top lines
# main.py
# main.py - Updated with graceful exit on Ctrl+C

from vm import create_vm
from docker import (
    create_dockerfile,
    build_docker_image,
    list_docker_images,
    list_running_containers,
    stop_container,
    search_local_image,
    search_dockerhub,
    pull_image
)
import sys

def main():
    print("=" * 50)
    print("     CLOUD MANAGEMENT SYSTEM")
    print("=" * 50)

    while True:
        print("\n1. Create Virtual Machine")
        print("2. Create Dockerfile")
        print("3. Build Docker Image")
        print("4. List Docker Images")
        print("5. List Running Containers")
        print("6. Stop a Container")
        print("7. Search Local Docker Image")
        print("8. Search Docker Hub")
        print("9. Pull Docker Image")
        print("0. Exit")

        try:
            choice = input("\nEnter choice: ").strip()
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            sys.exit(0)

        if choice == "1":
            create_vm()
        elif choice == "2":
            create_dockerfile()
        elif choice == "3":
            build_docker_image()
        elif choice == "4":
            list_docker_images()
        elif choice == "5":
            list_running_containers()
        elif choice == "6":
            stop_container()
        elif choice == "7":
            search_local_image()
        elif choice == "8":
            search_dockerhub()
        elif choice == "9":
            pull_image()
        elif choice == "0":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)