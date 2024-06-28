from utils.git_utils import get_git_diff, get_last_commit_messages
from utils.api_utils import call_api
from utils.string_shenanigans import clean_commit_message


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
    return call_api(url, headers, meta_prompt)


def generate_commit_message_examples(diff_analysis, diff, last_commits_summary, long=True):
    url = "http://localhost:11434/api/generate"
    headers = {'Content-Type': 'application/json'}
    commit_message_prompt = f"""Please generate 5 concise git commit message examples for the following diff, following the conventional commit format.

    Guidelines:
    1. Use one of these types: feat, fix, docs, style, refactor, test, chore.
    2. Keep the summary under 50 characters.
    3. Focus on the main change and its impact.
    4. If the commit change is big, provide a description in the body.
    5. If this commit is likely to have a great impact, point out its major achievements.
    6. If there is only minor refactoring, you should classify it as refactor.
    7. Do not include any additional text, explanations, or backticks.

    Here's the analysis of the diff:
    {diff_analysis}

    And here's the full git diff for reference:
    {diff}

    For additional context, here's a summary of the last few commit messages:
    {last_commits_summary}

    Please focus primarily on the current diff and its analysis when generating the commit message examples. 
    Use the last commit messages only for high-level context, but ensure the examples are specific to the current changes.

    Please provide your commit message examples in the following format:
    """
    if long:
        commit_message_prompt += f"""
        - <type>(<optional scope>): <short summary>
        <optional body>
        """
    else:
        commit_message_prompt += f"""
        - <type>(<optional scope>): <short summary>
        """
    commit_message_prompt += f"""
    Commit message examples:"""
    return call_api(url, headers, commit_message_prompt)

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
    return call_api(url, headers, selection_prompt)


def generate_commit_message(diff, logging=True, markdown=False):
    try:
        last_commits_summary = get_last_commit_messages()
        if logging: print(f"[Last Commit Messages]\n{last_commits_summary}")
        diff_analysis = analyze_diff(diff)
        if logging: print(f"[Diff Analysis]\n{diff_analysis}")
        commit_message_examples = generate_commit_message_examples(diff_analysis, diff, last_commits_summary)
        if logging: print(f"\n[Commit Message Examples]\n{commit_message_examples}")
        selected_commit_message = select_best_commit_message(commit_message_examples)
        selected_commit_message = clean_commit_message(selected_commit_message)
        if logging: print(f"\n[Selected Commit Message]\n{selected_commit_message}")
        markdown_logs = f"# Diff Analysis\n{diff_analysis}\n\n# Commit Message Examples\n{commit_message_examples}\n\n# Selected Commit Message\n{selected_commit_message}"
        if markdown:
            with open("commit_message.md", "w") as f:
                f.write(markdown_logs)
        return selected_commit_message
    except Exception as e:
        return f"Error: Failed to generate commit message. {str(e)}"
