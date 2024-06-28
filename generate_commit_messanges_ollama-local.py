import subprocess

import pyperclip
import requests
import re


def get_git_diff():
    try:
        result = subprocess.run(["git", "diff", "--cached"],
                                capture_output=True,
                                text=True,
                                check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: Git command failed. {e.stderr}"
    except FileNotFoundError:
        return "Error: Git is not installed or not in the system PATH."


def analyze_diff(diff):
    url = "http://localhost:11434/api/generate"
    headers = {'Content-Type': 'application/json'}

    meta_prompt = f"""You are an AI assistant skilled in analyzing git diffs and providing context for commit message generation.
    Please analyze the following git diff and provide a summary of the changes, including:
    1. The main areas of the code that are affected by the changes.
    2. Any notable modifications or additions to the code.
    3. Potential impact of the changes on the overall functionality. 
    4. If there is a large achievement, highlight its importance and explain it. Then add the recommendation to include it in the commit message.

    Here's the full git diff:
    {diff}

    Please provide your analysis as a concise summary, focusing on the most relevant information for generating a meaningful commit message.
    """

    diff_analysis = requests.post(url, headers=headers, json={
        "model": "llama3:instruct",
        "prompt": meta_prompt,
        "stream": False
    }).json()['response'].strip()

    return diff_analysis


def generate_commit_message_examples(diff_analysis, diff, long=True):
    url = "http://localhost:11434/api/generate"
    headers = {'Content-Type': 'application/json'}

    commit_message_prompt = f"""Please generate 5 concise git commit message examples for the following diff, following the conventional commit format.

    Guidelines:
    1. Use one of these types: feat, fix, docs, style, refactor, test, chore.
    2. Follow the format: <type>(<optional scope>): <short summary>
    3. Keep the summary under 50 characters.
    4. Focus on the main change and its impact.
    5. If the commit change is big, provide a description in the body.
    6. If this commit is likely to have a big impact, point out its major achievements.
    5. Do not include any additional text, explanations, or backticks.

    Here's the analysis of the diff:
    {diff_analysis}

    And here's the full git diff for reference:
    {diff}

    Please provide your commit message examples in the following format:
    """
    if long:
        commit_message_prompt += f"""
        - <type>(<optional scope>): <short summary>\n<optional body>
        """
    else:
        commit_message_prompt += f"""
        - <type>(<optional scope>): <short summary>
        """

    commit_message_prompt += f"""
    Commit message examples:"""

    commit_message_examples = requests.post(url, headers=headers, json={
        "model": "llama3:instruct",
        "prompt": commit_message_prompt,
        "stream": False
    }).json()['response'].strip()

    return commit_message_examples


def select_best_commit_message(commit_message_examples):
    url = "http://localhost:11434/api/generate"
    headers = {'Content-Type': 'application/json'}

    selection_prompt = f"""Please select the most appropriate commit message from the following examples:
    {commit_message_examples}

    Consider the following criteria when making your selection:
    1. Adherence to the conventional commit format.
    2. Clarity and conciseness of the summary.
    3. Relevance to the main changes in the diff.

    Please provide only the selected commit message, without any additional text or explanations.

    Selected commit message:"""

    selected_commit_message = requests.post(url, headers=headers, json={
        "model": "llama3:instruct",
        "prompt": selection_prompt,
        "stream": False
    }).json()['response'].strip()

    return selected_commit_message


def generate_commit_message(diff, logging=True):
    try:

        diff_analysis = analyze_diff(diff)
        if logging: print(f"[Diff Analysis]\n{diff_analysis}")
        commit_message_examples = generate_commit_message_examples(diff_analysis, diff)
        if logging: print(f"\n[Commit Message Examples]\n{commit_message_examples}")
        selected_commit_message = select_best_commit_message(commit_message_examples)
        if logging: print(f"\n[Selected Commit Message]\n{selected_commit_message}")
        markdown_logs = f"# Diff Analysis\n{diff_analysis}\n\n# Commit Message Examples\n{commit_message_examples}\n\n# Selected Commit Message\n{selected_commit_message}"
        if logging:
            with open("commit_message.md", "w") as f:
                f.write(markdown_logs)
        return selected_commit_message
    except requests.RequestException as e:
        return f"Error: Failed to generate commit message. {str(e)}"


if __name__ == "__main__":
    diff = get_git_diff()
    if diff.startswith("Error"):
        print(diff)
    else:
        commit_message = generate_commit_message(diff)

        # Copy the commit message to clipboard
        pyperclip.copy(commit_message)
        print(
            "\nCommit message has been copied to clipboard. You can now paste it into PyCharm's commit message field.")
