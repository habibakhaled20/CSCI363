import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext, simpledialog
import json
import os
import vm      
import docker  

class CloudManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cloud Management System")
        self.root.geometry("850x750")
        self.root.configure(bg="#f0f0f0")

        tk.Label(root, text="Cloud Management System", font=("Arial", 20, "bold"), bg="#f0f0f0").pack(pady=10)

        # Dashboard Buttons
        btn_frame = tk.Frame(root, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        self.add_btn(btn_frame, "Create VM (Interactive)", self.start_vm_wizard, 0, 0)
        self.add_btn(btn_frame, "Create VM (Config)", self.gui_vm_config, 0, 1)
        self.add_btn(btn_frame, "Create Dockerfile", self.gui_dockerfile, 1, 0)
        self.add_btn(btn_frame, "Build Docker Image", self.gui_build_image, 1, 1)
        self.add_btn(btn_frame, "List Docker Images", self.gui_list_images, 2, 0)
        self.add_btn(btn_frame, "List Running Containers", self.gui_list_containers, 2, 1)
        self.add_btn(btn_frame, "Stop Container", self.gui_stop_container, 3, 0)
        self.add_btn(btn_frame, "Search DockerHub", self.gui_search_hub, 3, 1)
        self.add_btn(btn_frame, "Search Image", self.gui_search_image, 3, 2)
        self.add_btn(btn_frame, "Pull Image", self.gui_pull_image, 4, 0)
        self.add_btn(btn_frame, "Run New Container", self.gui_run_container, 4, 1)

        self.output_area = scrolledtext.ScrolledText(root, width=95, height=20, bg="black", fg="white", font=("Consolas", 10))
        self.output_area.pack(pady=10)

    def add_btn(self, frame, text, cmd, r, c):
        tk.Button(frame, text=text, width=25, height=2, command=cmd).grid(row=r, column=c, padx=5, pady=5)

    def log(self, message):
        self.output_area.insert(tk.END, f"{message}\n")
        self.output_area.see(tk.END)

    # --- WIZARD NAVIGATION (Ensures 'Back' capability) ---
    def open_wizard(self, title):
        self.wizard_win = tk.Toplevel(self.root)
        self.wizard_win.title(title)
        self.wizard_win.geometry("400x350")
        self.wizard_win.grab_set()  # Pin to front
        self.wizard_frame = tk.Frame(self.wizard_win)
        self.wizard_frame.pack(expand=True, fill="both", padx=20, pady=20)

    def clear_wizard(self):
        for widget in self.wizard_frame.winfo_children():
            widget.destroy()

    def start_vm_wizard(self):
        self.vm_data = {"name": "ubuntu_vm", "cpu": "2", "ram": "2048", "disk": "20", "iso": ""}
        self.open_wizard("VM Creation Wizard")
        self.vm_step_1()

    def vm_step_1(self):
        self.clear_wizard()
        tk.Label(self.wizard_frame, text="Step 1: Enter VM Name", font=("Arial", 10, "bold")).pack(pady=10)
        ent = tk.Entry(self.wizard_frame)
        ent.insert(0, self.vm_data["name"])
        ent.pack(pady=5)
        
        tk.Button(self.wizard_frame, text="Next", width=10, 
                  command=lambda: [self.vm_data.update({"name": ent.get()}), self.vm_step_2()]).pack(side="bottom", pady=10)

    def vm_step_2(self):
        self.clear_wizard()
        tk.Label(self.wizard_frame, text="Step 2: Hardware Settings", font=("Arial", 10, "bold")).pack(pady=5)
        tk.Label(self.wizard_frame, text="CPU Cores:").pack()
        c_ent = tk.Entry(self.wizard_frame); c_ent.insert(0, self.vm_data["cpu"]); c_ent.pack()
        tk.Label(self.wizard_frame, text="RAM (MB):").pack()
        r_ent = tk.Entry(self.wizard_frame); r_ent.insert(0, self.vm_data["ram"]); r_ent.pack()

        btn_f = tk.Frame(self.wizard_frame)
        btn_f.pack(side="bottom", pady=10)
        tk.Button(btn_f, text="Back", command=self.vm_step_1).pack(side="left", padx=5)
        tk.Button(btn_f, text="Next", command=lambda: [self.vm_data.update({"cpu": c_ent.get(), "ram": r_ent.get()}), self.vm_step_3()]).pack(side="left", padx=5)

    def vm_step_3(self):
        self.clear_wizard()
        tk.Label(self.wizard_frame, text="Step 3: Disk & ISO", font=("Arial", 10, "bold")).pack(pady=5)
        tk.Label(self.wizard_frame, text="Disk Size (GB):").pack()
        d_ent = tk.Entry(self.wizard_frame); d_ent.insert(0, self.vm_data["disk"]); d_ent.pack()
        tk.Button(self.wizard_frame, text="Browse ISO File", command=self.browse_iso).pack(pady=10)
        
        btn_f = tk.Frame(self.wizard_frame)
        btn_f.pack(side="bottom", pady=10)
        tk.Button(btn_f, text="Back", command=self.vm_step_2).pack(side="left", padx=5)
        tk.Button(btn_f, text="Finish", bg="#2ecc71", command=lambda: self.finish_vm(d_ent.get())).pack(side="left", padx=5)

    def browse_iso(self):
        path = filedialog.askopenfilename(title="Select ISO", filetypes=[("ISO Files", "*.iso")])
        if path: self.vm_data["iso"] = path

    def finish_vm(self, disk_val):
        self.vm_data["disk"] = disk_val
        self.log(f"Launching {self.vm_data['name']}...")
        status = vm.launch_vm_logic(self.vm_data["name"], self.vm_data["cpu"], self.vm_data["ram"], self.vm_data["disk"], self.vm_data["iso"])
        self.log(status)
        self.wizard_win.destroy()

    # --- DOCKER FUNCTIONS ---
    def gui_dockerfile(self):
        self.open_wizard("Dockerfile Wizard")
        self.clear_wizard()
        tk.Label(self.wizard_frame, text="Save Path:").pack()
        p_ent = tk.Entry(self.wizard_frame); p_ent.insert(0, "Dockerfile"); p_ent.pack()
        tk.Label(self.wizard_frame, text="Contents:").pack()
        txt = tk.Text(self.wizard_frame, height=10, width=45)
        txt.insert("1.0", "FROM ubuntu\nRUN apt-get update\nCMD [\"bash\"]")
        txt.pack(pady=5)

        tk.Button(self.wizard_frame, text="Save & Create", bg="#2ecc71", 
                  command=lambda: [self.log(docker.create_dockerfile_logic(p_ent.get(), txt.get("1.0", tk.END))), self.wizard_win.destroy()]).pack()

    def gui_build_image(self):
        tag = simpledialog.askstring("Input", "Enter image name:tag:", parent=self.root)
        if tag:
            self.log(f"Building {tag}... Please wait.")
            status = docker.build_image_logic(tag)
            self.log(status) 

    def gui_run_container(self):
        tag = simpledialog.askstring("Input", "Enter Image Name to Run:", parent=self.root)
        if tag:
            self.log(f"Starting container from {tag}...")
            self.log(docker.run_container_logic(tag))

    def gui_list_containers(self):
        self.log("\n--- Running Containers ---\n" + docker.list_running_containers())

    def gui_list_images(self):
        self.log("\n--- Docker Images ---\n" + docker.list_docker_images())

    def gui_vm_config(self):
        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if path:
            try:
                with open(path, "r", encoding='utf-8') as f:
                    data = json.load(f)
                status = vm.launch_vm_logic(data['name'], data['cpu'], data['ram'], data['disk'], data['iso'])
                self.log(status)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load config: {e}")

    def gui_stop_container(self):
        cid = simpledialog.askstring("Input", "Enter Container ID:", parent=self.root)
        if cid: self.log(docker.stop_container_logic(cid))

    def gui_search_hub(self):
        q = simpledialog.askstring("Input", "Search term:", parent=self.root)
        if q: self.log(docker.search_hub_logic(q))

    def gui_search_image(self):
        q = simpledialog.askstring("Input", "Enter image name or tag to search locally:", parent=self.root)
        if q:
            self.log(f"\n--- Local Image Search: {q} ---\n")
            self.log(docker.search_local_images_logic(q))

    def gui_pull_image(self):
        img = simpledialog.askstring("Input", "Image to pull (e.g., nginx):", parent=self.root)
        if img:
            self.log(f"Pulling {img} from DockerHub...")
            status = docker.pull_image_logic(img)
            self.log(status)

if __name__ == "__main__":
    root = tk.Tk()
    app = CloudManagerGUI(root)
    root.mainloop()