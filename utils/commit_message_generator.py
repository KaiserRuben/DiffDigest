from utils.git_utils import get_last_commit_messages
from utils.api_utils import call_api
from utils.string_shenanigans import clean_commit_message
from tqdm import tqdm


def analyse_last_commit_messages(history, diff):
    last_commits_prompt = """
    Given a git history and a git diff, analyse the history of the now changed code.
    Highlighting the most significant relationships and insights between the commits and the given change.
    If possible, follow the history of the code and explain the changes on the way, inbetween quoting the referenced commit messages.
        """

    last_commits_prompt += f"""
    \n\n[DATA]
    [HISTORY]
    {history}
    [/HISTORY]\n\n
    [DIFF]
    {diff}
    [/DIFF]
    [/DATA]
    """

    return call_api(last_commits_prompt)


def analyze_diff(diff):
    meta_prompt = f"""You are an AI assistant skilled in analyzing git diffs and providing context for commit message generation.
    Please analyze the following git diff and provide a summary of the changes, including:
    1. The main areas of the code that are affected by the changes.
    2. If its just reformatting, mention it.
    3. Any notable modifications or additions to the code.
    4. Potential impact of the changes on the overall functionality. 
    5. If there is a large change, highlight its importance and explain it. Then add the recommendation to include it in the commit message.

    Here's the full git diff:
    {diff}

    Please provide your analysis as a concise summary, focusing on the most relevant information for generating a meaningful commit message that includes all relevant aspects. Do not provide an example for the commit message, focus on the analysis.
    """
    return call_api(meta_prompt)


def gather_commit_message_info(diff_analysis, diff, last_commits_summary):
    info_gathering_prompt = f"""Please provide the following information to help generate a commit message:

    1. Main changes: Briefly summarize the main changes in the diff.
    2. Impact: Assess the potential impact of these changes (minor, moderate, or significant).
    3. Type: Suggest the most appropriate commit type (feat, fix, docs, style, refactor, test, chore).
    4. Scope: If applicable, suggest a scope for the commit (e.g., component or module name).
    5. Continuation: Determine if the current changes are a continuation of a previous task or feature mentioned in the last commit messages.

    Here's the analysis of the diff:
    {diff_analysis}

    And here's the full git diff for reference:
    {diff}

    For additional context, here's an analysis of the last few commit messages:
    {last_commits_summary}

    Please provide the information in the following format:
    Main changes: <brief summary>
    Impact: <minor/moderate/significant>
    Type: <type>
    Scope: <optional scope>
    Continuation: <yes/no>
    """
    return call_api(info_gathering_prompt)


def final_generate_message(commit_message_info, long=True):
    commit_message_prompt = f"""
    Generate a git commit message based on the following information:

    {commit_message_info}

    Guidelines:
    1. Use the suggested type and scope (if provided).
    2. Keep the summary under 50 characters.
    3. If the impact is moderate or significant, provide a description in the body, which may be longer.
    4. If the changes are a continuation of a previous task, consider using phrases like "continued fixing feature x" or "continued refactoring".
    5. Provide only the commit message itself, without any additional text, explanations, or formatting. Never start your answer with "commit message:", "Here is ..." or any other prefix. 
    6. Start with fest, fix, docs, style, refactor, test, chore, etc.

    Format:
    """

    if long:
        commit_message_prompt += f"""
    <type>(<optional scope>): <short summary>

    <optional body>
    """
    else:
        commit_message_prompt += f"""
    <type>(<optional scope>): <short summary>
    """

    return call_api(commit_message_prompt)


def generate_commit_message(diff: str, logging: bool = True, markdown: bool = False) -> str:
    """
    Generate a commit message based on the provided diff.

    Args:
        diff (str): The diff string representing the changes.
        logging (bool, optional): Whether to log the process. Defaults to True.
        markdown (bool, optional): Whether to write the logs to a markdown file. Defaults to False.

    Returns:
        str: The generated commit message or an error message if an exception occurs.
    """
    try:
        with tqdm(total=4, desc="Generating Commit Message") as pbar:
            history = get_last_commit_messages()
            last_commits_summary = analyse_last_commit_messages(history, diff)
            if logging:
                print(f"[Last Commit Messages]\n{last_commits_summary}")
            pbar.update(1)

            diff_analysis = analyze_diff(diff)
            if logging:
                print(f"[Diff Analysis]\n{diff_analysis}")
            pbar.update(1)

            commit_message_examples = gather_commit_message_info(diff_analysis, diff, last_commits_summary)
            if logging:
                print(f"\n[Commit Message Examples]\n{commit_message_examples}")
            pbar.update(1)

            selected_commit_message = final_generate_message(commit_message_examples)
            selected_commit_message = clean_commit_message(selected_commit_message)
            if logging:
                print(f"\n[Selected Commit Message]\n{selected_commit_message}")
            pbar.update(1)

            markdown_logs = f"# Diff Analysis\n{diff_analysis}\n\n# Commit Message Examples\n{commit_message_examples}\n\n# Selected Commit Message\n{selected_commit_message}"
            if markdown:
                try:
                    with open("commit_message.md", "w") as f:
                        f.write(markdown_logs)
                except Exception as e:
                    return f"Error: Failed to write markdown logs to file. {str(e)}"

            return selected_commit_message
    except Exception as e:
        return f"Error: Failed to generate commit message. {str(e)}"
