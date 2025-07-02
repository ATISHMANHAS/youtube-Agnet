import subprocess

print("--- FOOFA AGENT FULL RUN STARTED ---\n")

scripts = ["videoselector.py", "clipper.py", "uploader.py"]

for script in scripts:
    print(f"Running: {script}")
    try:
        result = subprocess.run(["python", script], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Error running", script + ":\n", result.stderr)
    except Exception as e:
        print(f"Exception running {script}: {e}")
