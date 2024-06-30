import pyperclip
from utils.git_utils import get_git_diff
from utils.commit_message_generator import generate_commit_message

if __name__ == "__main__":
    diff = get_git_diff()
    if diff.startswith("Error"):
        print(diff)
    elif not diff:
        print("No changes detected.")
    else:
        commit_message = generate_commit_message(diff)
        pyperclip.copy(commit_message)
        print("\nCommit message has been copied to clipboard. You can now paste it into PyCharm's commit message field.")