# AI Coding Agent

A command-line coding agent written in Python, built as part of the Boot.dev backend curriculum. You give it a task in plain English, and it uses Google's Gemini API with function calling to explore a project, read and edit files, and run Python scripts until the task is done.

The agent works inside a bundled sample project, a small command-line calculator in `calculator/`, so you can try it safely on code that is meant to be changed.

## Features

- Takes a natural-language task from the command line
- Plans and acts through **function calling**: the model chooses which tool to call, and the results are fed back to it
- Four tools: list directories, read files, write files, and run Python files
- Agent loop that keeps going until the model gives a final answer, with a cap on the number of iterations
- Path validation so file tools cannot reach outside the working directory
- 30-second timeout on executed scripts
- `--verbose` mode that shows token usage, each function call with its arguments, and each result

## How It Works

1. Your prompt is sent to Gemini along with a system prompt and the declarations of the four tools.
2. If the model replies with function calls, the agent runs each one and sends the results back to the model as the next message.
3. This repeats until the model replies with plain text, which is printed as the final response.
4. If the model has not finished after 20 iterations, the agent prints an error and exits.

The working directory is never chosen by the model. The agent injects it into every tool call, so the model only supplies paths relative to it.

## Prerequisites

- Python 3.13 or later
- A Gemini API key from [Google AI Studio](https://aistudio.google.com)
- [uv](https://docs.astral.sh/uv/) (recommended), or `pip`

## Setup

```bash
git clone https://github.com/Ravinder2102/AI_agent.git
cd AI_agent
```

Create a `.env` file in the project root with your API key:

```env
GEMINI_API_KEY="your-api-key"
```

The `.env` file is listed in `.gitignore`, so it won't be committed. Never commit your key.

Install the dependencies:

```bash
uv sync
```

Without uv:

```bash
pip install google-genai==1.12.1 python-dotenv==1.1.0
```

## Usage

Run the agent from the project root with a prompt in quotes:

```bash
uv run main.py "your task here"
```

Add `--verbose` to see token counts and every function call:

```bash
uv run main.py "your task here" --verbose
```

Without uv, use `python main.py "your task here"` instead.

### Example prompts

```bash
uv run main.py "what files are in the project?"
uv run main.py "run the calculator with the expression 3 + 5"
uv run main.py "run the tests and tell me if any fail"
uv run main.py "explain how the calculator handles operator precedence"
uv run main.py "add a unit test for division by zero" --verbose
```

Run the command from the repository root, because the working directory is set to `./calculator` relative to where you start the program.

## Tools

| Tool               | What it does                                                           |
| ------------------ | ---------------------------------------------------------------------- |
| `get_files_info`   | Lists files in a directory with their sizes and whether they are folders |
| `get_file_content` | Reads a file, returning at most 10,000 characters and marking truncation |
| `write_file`       | Creates or overwrites a file, creating parent folders if needed        |
| `run_python_file`  | Runs a `.py` file with optional arguments and returns stdout and stderr |

## Safety and Limitations

- **File tools are restricted by path checks.** Every path is resolved to an absolute path and rejected if it falls outside the working directory, which blocks attempts like `../` and absolute paths such as `/bin`.
- **Running code is not sandboxed.** `run_python_file` starts a normal `python` process in the working directory with a 30-second timeout. The path check only validates which file is launched. Once running, a script can do anything your user account can do. Only run the agent on code you trust, and ideally inside a container or virtual machine.
- **The agent can modify and overwrite files** in the working directory, so keep a copy or use version control.
- **The working directory is fixed** to `./calculator` in `call_function.py`. To use the agent on another project, change that value.
- **Results depend on the model.** The agent may misread code, make wrong edits, or hit the 20-iteration limit on harder tasks.
- **Tests are manual scripts.** The `test_*.py` files in the root print results for you to inspect, rather than asserting them.

## Configuration

Settings live in `config.py`:

| Setting     | Default | Meaning                                        |
| ----------- | ------- | ---------------------------------------------- |
| `MAX_CHARS` | 10000   | Maximum characters returned when reading a file |
| `MAX_ITERS` | 20      | Maximum model calls for a single prompt        |

The model is `gemini-2.5-flash`, set in `main.py`, and the script timeout is 30 seconds in `functions/run_python_file.py`.

## Testing

Run a manual test script for a tool and check its output, for example:

```bash
uv run test_get_files_info.py
uv run test_write_file.py
```

These include cases that should be refused, such as paths outside the working directory.

The sample calculator has its own unit tests:

```bash
cd calculator
python -m unittest tests.py
```

Note that `test_write_file.py` overwrites `calculator/lorem.txt` and `calculator/pkg/morelorem.txt`, so run `git checkout calculator` afterwards if you want them restored.

## Built With

- [Python](https://www.python.org)
- [google-genai](https://pypi.org/project/google-genai/) for the Gemini API
- [python-dotenv](https://pypi.org/project/python-dotenv/) for loading the API key
- [uv](https://docs.astral.sh/uv/) for dependency management