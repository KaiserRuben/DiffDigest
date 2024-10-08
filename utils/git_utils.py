import os
import subprocess
import logging

import config

logging.basicConfig(level=logging.ERROR)


def get_git_diff():
    try:
        result = subprocess.run(["git", "diff", "--cached"],
                                capture_output=True,
                                text=True,
                                check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"Git command failed: {e}")
        logging.error(f"stdout: {e.stdout}")
        logging.error(f"stderr: {e.stderr}")
        logging.error(f"returncode: {e.returncode}")
        return f"Error: Git command failed. {e.stderr}"
    except FileNotFoundError:
        logging.error("Git is not installed or not in the system PATH")
        return "Error: Git is not installed or not in the system PATH."


def get_last_commit_messages(num_commits=config.MAX_COMMITS):
    try:
        output = subprocess.check_output(["git", "log", f"-p", f"-n{num_commits}"], encoding='utf-8', errors='replace')
        commit_messages = output.strip().split("\n")
        return "\n".join(commit_messages)
    except subprocess.CalledProcessError as e:
        return f"Error: Failed to retrieve last commit messages. {str(e)}"
