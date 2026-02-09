# RepoLens: AI-Powered Code Audit

RepoLens is a command-line tool that scans a local project directory, aggregates the source code, and uses the Google Gemini model to generate a comprehensive architectural audit report.

## Features

*   **AI-Powered Analysis:** Leverages Google's Gemini models to provide insights on architecture, design patterns, and code quality.
*   **Simple CLI:** An easy-to-use command-line interface built with Typer and Rich.
*   **API Retry Logic:** Automatically retries API calls on transient errors to improve reliability.
*   **Dry-Run Mode:** Preview which files will be analyzed without making any API calls.
*   **Organized Output:** Saves reports to a dedicated `reports/` directory with versioned filenames.

## Instalacja

1.  **Clone the repository:**

    ```bash
    git clone <your-repository-url>
    cd RepoLens
    ```

2.  **Install dependencies:**

    ```bash
    pip install google-generativeai python-dotenv "typer[all]"
    ```

## Configuration

1.  Create a `.env` file in the project's root directory.

2.  Add your Google Gemini API key to the `.env` file:

    ```
    GEMINI_API_KEY="your_api_key_here"
    ```

## Użycie

*   **Run a full analysis:**
    `python main.py /path/to/your/project`

*   **Use a specific model:**
    `python main.py /path/to/your/project --model "gemini-1.5-pro-latest"`

*   **Perform a dry run:**
    `python main.py /path/to/your/project --dry-run`

*   **List available models:**
    `python list_models.py`

## Output

Analysis reports are saved in the `reports/` directory with versioned filenames (e.g., `my-project_report_1.md`) to prevent overwriting previous results.
