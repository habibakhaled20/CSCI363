# src/vm/main.py
from vm import create_vm          # Simple relative import
from docker import *              # or from docker import function names
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

        choice = input("\nEnter choice: ").strip()

        if choice == "1": create_vm()
        elif choice == "2": create_dockerfile()
        elif choice == "3": build_docker_image()
        elif choice == "4": list_docker_images()
        elif choice == "5": list_running_containers()
        elif choice == "6": stop_container()
        elif choice == "7": search_local_image()
        elif choice == "8": search_dockerhub()
        elif choice == "9": pull_image()
        elif choice == "0":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()