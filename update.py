import os
import subprocess

os.environ["PATH"] += r";C:\Program Files\Git\cmd"
subprocess.run(["git", "add", "."], check=True)
subprocess.run(["git", "commit", "-m", "Fix mobile responsiveness and layout overflow for Bond Calculator"], check=True)
subprocess.run(["git", "push", "origin", "main"], check=True)
print("Pushed successfully!")
