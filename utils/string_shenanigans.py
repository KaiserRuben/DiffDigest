import re


def clean_commit_message(commit_message):
    # Remove leading backticks, asterisks, and newline characters
    # cleaned_message = re.sub(r'^[`*]{1,4}\n?', '', commit_message)
    cleaned_message = re.sub(r'[\n`*]{1,3}', '', commit_message)

    # Strip any leading or trailing whitespace
    cleaned_message = cleaned_message.strip()

    return cleaned_message