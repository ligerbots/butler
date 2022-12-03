import os
import json
import subprocess

f_config = open('config/config.json', 'r')

print("Loading data from config.json")
data = json.load(f_config)
print("Data loaded")

# TO-DO: Maybe add some comparison to a template here to ensure you have everything?

print("Setting environment variables")
for key in data:
    print(f"SET env var: {key}")
    subprocess.Popen(["export", f"{key}={data[key]}"], shell=True)

print("All environment variables set")
print("COMPLETED")

