# Linux Command Helper

A Python-based utility that leverages the Google Gemini API to identify relevant Linux commands based on a user's natural language description 
and retrieves their usage documentation using `tldr`.

## Features

- **AI-Powered Discovery:** Uses Gemini to map natural language queries to executable Linux commands.
- **Caching:** Local JSON caching to reduce API calls and improve performance for repeated queries.
- **Documentation Retrieval:** Automatically fetches command documentation via `tldr`.
- **Intelligent Normalization:** Filters out stop-words to improve cache hit rates.

## Prerequisites

1. **Python 3.10+**
2. **Google Gemini API Key:** Get one from [Google AI Studio](https://aistudio.google.com/).
3. **`tldr` installed:** Ensure the `tldr` client is installed on your Linux system.
   ```bash
   sudo apt install tldr

## Installation

Clone the repository.

Install the required dependencies:

`pip install -r requirements.txt`

Create a .env file in the root directory and add your API key:

`GOOGLE_API_KEY=your_actual_api_key_here`

## Usage

Run the script by passing your intent as a string argument:

`python main.py "How do I check my network interfaces?"`

## How it works:

- The app parses your input and sends it to the Gemini API to determine the most relevant command names.

- It checks a local file (get_cmd.json) to see if you have searched for this context before.

- If valid commands are found, it uses tldr <command> to print documentation directly to your terminal.

## Dependencies

google-genai: Official Google Generative AI SDK.

python-dotenv: For secure environment variable management.

httpx: For handling network requests.
