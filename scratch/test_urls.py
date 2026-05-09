import subprocess
import os

print("Running pipeline.py...")
subprocess.run(["python", "scripts/pipeline.py"], check=True)

print("Running daily_digest.py...")
subprocess.run(["python", "scripts/daily_digest.py"], check=True)
