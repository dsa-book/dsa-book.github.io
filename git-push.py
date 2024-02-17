import sys
import subprocess

def push(commit_message):
    subprocess.run(["git", "add", "*"], check=True)
    subprocess.run(["git", "add", "./*"], check=True)
    subprocess.run(["git", "commit", "-m", commit_message], check=True)
    subprocess.run(["git", "push"], check=True)

if __name__ == "__main__":
    commit_message = sys.argv[1]
    push(commit_message)
