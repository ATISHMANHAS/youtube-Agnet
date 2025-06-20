# run_agent.py
import subprocess

scripts = ["videoselector.py", "clipper.py", "uploader.py"]

print("\n--- FOOFA AGENT FULL RUN STARTED ---\n")

for script in scripts:
    print(f"Running: {script}")
    try:
        result = subprocess.run(["python", script], check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Warnings:\n", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script}:\n{e.stderr}")

print("\n--- ALL DONE ---")
