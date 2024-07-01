# DiffDigest: Git Commit Message Generator

The Git Commit Message Generator is a Python-based tool that helps developers create meaningful and standardized commit messages based on the changes in their Git repository. It analyzes the Git diff, generates commit message examples, and selects the most appropriate message for the user to use.

## Features

- Retrieves the Git diff of the staged changes
- Analyzes the diff to provide a summary of the affected areas, notable modifications, and potential impact
- Generates commit message examples following the conventional commit format
- Selects the most appropriate commit message based on relevance and clarity
- Copies the selected commit message to the clipboard for easy pasting into the commit message field
- Supports multiple LLM providers for flexible and powerful language processing

## Requirements

- Python 3.6 or higher
- Git installed and accessible from the system PATH
- Python packages: `requests`, `pyperclip`


## LLM Provider Setup

DiffDigest supports multiple LLM (Large Language Model) providers. You can choose between Anthropic (Claude), OpenAI, and Ollama. Each provider has its own advantages and considerations.

### Anthropic (Claude) - Recommended
- Sign up for an Anthropic account and obtain an API key at [https://www.anthropic.com](https://www.anthropic.com) or [https://console.anthropic.com](https://console.anthropic.com).
- Set the `ANTHROPIC_API_KEY` environment variable with your API key.

Advantages:
- Superior performance in understanding context and generating nuanced responses
- Strong ethical considerations and safety measures built into the model
- Consistent and reliable outputs

Disadvantages:
- May be more expensive compared to other options
- Requires an internet connection to access the API

### OpenAI
- Sign up for an OpenAI account and obtain an API key at [https://platform.openai.com/signup](https://platform.openai.com/signup).
- Set the `OPENAI_API_KEY` environment variable with your API key.

Disadvantages:
- Can be expensive for high-volume usage
- Requires an internet connection to access the API
- Wordy, will lead to longer commit messages

### Ollama
- Install Ollama from the [official website](https://ollama.com/).
- Pull the Model of your choice using the following command:
  ```bash
  ollama pull <model_name>
  ```
- Make sure that Ollama is running in the background by executing:
  ```bash
  ollama start
  ```

Advantages:
- Runs locally, providing better privacy and offline capabilities
- No usage costs beyond initial setup
- Allows for easy switching between different open-source models

Disadvantages:
- May have lower performance compared to cloud-based options
- Requires more powerful local hardware for optimal performance
- Limited to available open-source models, which may not be as advanced as proprietary ones

## Configuration

Edit the `config.py` file to choose your desired LLM service:

```python
# Choose the desired LLM service
LLM_SERVICE = AnthropicService(ANTHROPIC_API_KEY, ANTHROPIC_MODEL)
# LLM_SERVICE = OpenAIService(OPENAI_API_KEY, OPENAI_MODEL)
# LLM_SERVICE = OLLAMAService(OLLAMA_URL, OLLAMA_MODEL)
```

Uncomment the line for your preferred service and ensure the necessary environment variables or configurations are set.

## Usage

1. Stage the changes you want to commit using `git add`.
2. Run the `main.py` script using Python.
3. The tool will analyze the Git diff, generate commit message examples, and select the most appropriate one.
4. The selected commit message will be copied to your clipboard.
5. Paste the commit message into your Git client's commit message field and proceed with the commit.

## Q&A

### How does the Git Commit Message Generator work?

The Git Commit Message Generator follows these steps:

1. Retrieves the Git diff of the staged changes using the `git diff --cached` command.
2. Analyzes the diff to provide a summary of the affected areas, notable modifications, and potential impact using an AI-powered API.
3. Generates commit message examples following the conventional commit format, considering the diff analysis and the last few commit messages for context.
4. Selects the most appropriate commit message based on relevance and clarity using the AI-powered API.
5. Cleans up the selected commit message by removing any unwanted characters or formatting.
6. Copies the selected commit message to the clipboard for easy pasting into the commit message field.

### How can I integrate the Git Commit Message Generator into my JetBrains IDE (PyCharm, IntelliJ IDEA, etc.)?

1. Open your JetBrains IDE and navigate to "File" -> "Settings" (or "IDE Name" -> "Preferences" on macOS).
2. Go to "Tools" -> "External Tools".
3. Click the "+" button to add a new external tool.
4. Fill in the following details:
  - Name: Git Commit Message Generator
  - Program: `python` (or the path to your Python executable)
  - Arguments: `path/to/main.py`
  - Working directory: `$ProjectFileDir$`
5. Click "OK" to save the external tool configuration.
6. Assign a keyboard shortcut to the external tool:
  - Go to "File" -> "Settings" -> "Keymap".
  - Search for the external tool name ("Git Commit Message Generator") in the search bar.
  - Right-click on the tool and select "Add Keyboard Shortcut".
  - Choose your desired keyboard shortcut and click "OK".
7. Now you can use the assigned keyboard shortcut to run the Git Commit Message Generator within your JetBrains IDE.

### How can I integrate the Git Commit Message Generator into Visual Studio Code (VSCode)?

1. Open VSCode and navigate to the "Extensions" view (Ctrl+Shift+X or Cmd+Shift+X).
2. Search for and install the "Command Runner" extension.
3. Open the VSCode settings (File -> Preferences -> Settings or Ctrl+,).
4. Search for "Command Runner" in the settings search bar.
5. Scroll down to "Command Runner: Commands" and click "Edit in settings.json".
6. Add the following configuration to the "command-runner.commands" array:
      ```json
      {
        "name": "Generate Git Commit Message",
        "command": "python",
        "args": ["path/to/main.py"]
      }
      ```
7. Save the settings.json file.
8. Open the VSCode keyboard shortcuts (File -> Preferences -> Keyboard Shortcuts or Ctrl+K Ctrl+S).
9. Search for "Generate Git Commit Message" in the search bar.
10. Click on the "+" button next to the command to assign a keyboard shortcut.
11. Press the desired key combination and click "Enter".
12. Now you can use the assigned keyboard shortcut to run the Git Commit Message Generator within VSCode.

## Building a Plugin

To make DiffDigest even more accessible, consider building plugins for popular development environments:

1. VSCode Extension:
   - Use the VSCode Extension API to create a dedicated DiffDigest extension.
   - Implement a sidebar view for commit message generation and selection.
   - Add custom commands for easy access to DiffDigest features.

2. JetBrains Plugin:
   - Utilize the IntelliJ Platform SDK to develop a plugin compatible with various JetBrains IDEs.
   - Create a tool window for DiffDigest functionality.
   - Integrate with the built-in VCS features of JetBrains IDEs.

3. Git GUI Client Plugins:
   - Develop plugins for popular Git GUI clients like GitKraken, SourceTree, or GitHub Desktop.
   - Implement DiffDigest as a native feature within these clients' commit workflows.

By building plugins, you can streamline the commit message generation process and make it an integral part of developers' workflows across different platforms and tools.

## License
This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License. To view a copy of this license, visit https://creativecommons.org/licenses/by-nc/4.0/