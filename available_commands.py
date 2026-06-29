import shutil
import subprocess

def cmd_details(commands):
    
    output = []
    for cmd in commands:
        if shutil.which(cmd):
            try:
                result = subprocess.run(["tldr", cmd], capture_output=True, text=True, check=True, encoding='utf-8')
                if result.returncode == 0:
                    output.append(result.stdout)
            except subprocess.CalledProcessError:
                print(f"Failed to fetch details for {cmd}")
            except FileNotFoundError:
                print("Tool 'tldr' not found, install with apt install tldr")
                raise SystemExit(1)
    return "\n".join(output)