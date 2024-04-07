import customtkinter as ctk
import os
import json
import subprocess
import threading
import urllib.request

current_directory = os.path.dirname(os.path.abspath(__file__))
# file_path = os.path.join(current_directory, "scripts_config.json")

def install_and_run(requirements_url, script_url, button):
    def install():
        button.configure(state=ctk.DISABLED, text="Instalowanie...")
        subprocess.run(["pip", "install", "-r", requirements_url])
        button.configure(text="Uruchom skrypt", state=ctk.NORMAL)
    def clear_log():
        log_text.configure(state=ctk.NORMAL)
        log_text.delete("1.0", ctk.END)
        log_text.configure(state=ctk.DISABLED) 
    def update_log():
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                log_text.configure(state=ctk.NORMAL)
                log_text.insert(ctk.END, output.strip() + "\n")
                log_text.configure(state=ctk.DISABLED)
                log_text.see(ctk.END)

    install_thread = threading.Thread(target=install)
    install_thread.start()

    urllib.request.urlretrieve(script_url, "script.py")
    process = subprocess.Popen(["pythonw", "script.py"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    log_text.configure(state=ctk.DISABLED)
    log_text.delete("1.0", ctk.END) 

    threading.Thread(target=clear_log).start()
    threading.Thread(target=update_log).start()

def load_config_from_github():
    github_raw_url = 'https://raw.githubusercontent.com/BartoszJakubowsky/Python/master/scripts_config.json'
    config_data = {}

    try:
        with urllib.request.urlopen(github_raw_url) as response:
            config_data = json.loads(response.read().decode())
    except Exception as e:
        print(f"Error loading config from GitHub: {e}")

    return config_data

def start_app():

    def create_ui(root):
        root.geometry("500x500")
        root.title("Script Runner by BartoszJakubowsky")

        label = ctk.CTkLabel(root, text="Script Runner App", font=("Helvetica", 16))
        label.pack(pady=10)

        log_text = ctk.CTkTextbox(root, height=300, width=400)
        log_text.pack(pady=5)

    def create_buttons(root):
        def get_scripts():
            config_data = load_config_from_github()
            scripts = config_data.get("scripts", [])
            return scripts
            # with open(file_path, "r") as file:
            #     config_data = json.load(file)
            #     scripts = config_data["scripts"]
        
        buttons = []
        scripts = get_scripts();
        for script in scripts:
            title = script["title"]
            script_url = script["script_url"]
            requirements_url = script["requirements"]

            button = ctk.CTkButton(root, text=title)
            button.pack(pady = 5)
            buttons.append(button)

            button.configure(command=lambda req_url=requirements_url, scr_url=script_url, btn=button: install_and_run(req_url, scr_url, btn))
    
    root = ctk.CTk()
    
    create_ui(root)
    create_buttons(root)

    root.mainloop()

start_app();