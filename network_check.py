import subprocess, os
from pathlib import Path
import json

data = {}

def main():
    global data

    if (Path('config.json').is_file()):
        with open('config.json') as data_file:
            data = json.load(data_file)
    else:
        generate_config_file()

    if is_in_work_network():
        launch_work_apps()
    elif is_in_home_network():
        launch_home_apps()
    else:
        print("not at work")
    # launch_work_apps()

def is_in_home_network():
    is_at_home = False
    home_networks = data["home"]["networks"]
    for networks in home_networks:
        if networks in subprocess.check_output("netsh wlan show interfaces").decode("utf-8"):
            is_at_home = True
            break
    return is_at_home

def is_in_work_network():
    is_at_work = False
    work_networks = data["work"]["networks"]
    for networks in work_networks:
        if networks in subprocess.check_output("netsh wlan show interfaces").decode("utf-8"):
            is_at_work = True
            break
    return is_at_work

def generate_config_file():
    global data
    data = {
      "home":
      {
        "networks": ["example_home_wifi"],
        "apps": ["example_home_app.exe"]
      },
      "work":
      {
        "networks": ["example_work_wifi"],
        "apps": ["example_work_app.exe"]
      },
      "public":
      {
        "networks": [],
        "apps": []
      }
    }
    new_file = open("config.json", "w")
    new_file.write(json.dumps(data))
    new_file.close()

def launch_home_apps():
    for apps in data["home"]["apps"]:
        p = subprocess.Popen(apps, close_fds=True)

def launch_work_apps():
    for apps in data["work"]["apps"]:
        p = subprocess.Popen(apps, close_fds=True)

if __name__ == "__main__":
    main()
