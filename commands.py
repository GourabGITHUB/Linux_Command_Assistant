from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError
import httpx
import logging
import os
import json
import re
from difflib import get_close_matches

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

logging.basicConfig(
    level = logging.INFO,
    format = "%(levelname)s | %(message)s"
    )

if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found")

client = genai.Client(api_key=API_KEY)

file = "get_cmd.json"

def load_cache():
    if not os.path.exists(file):
        with open(file, 'w') as f:
            pass
    try:
        with open(file, 'r')as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}
def save_cache(cache):
    with open(file, 'w') as f:
        json.dump(cache, f, indent=4)
        
        
STOP_WORDS = {
    "show", "display", "list", "check",
    "view", "get", "find", "print", "fix"
}

def normalize(text: str) -> str:
    text = re.sub(r"[^\w\s]", "", text.lower().strip())
    text = re.sub(r"\s+", " ", text)
    text = re.findall(r"\w+", text)
    return " ".join(t for t in text if t not in STOP_WORDS)


def get_cmd(context: str) -> list[str]:
    try:
        prompt = (
            f"""You are a Linux expert.

                Task:
                {context}

                Rules:
                - Return ONLY executable command names.
                - Do NOT include arguments, flags, subcommands, pipes, or shell syntax.
                - Examples:
                  Correct:
                  systemctl
                  ip
                  ss
                  journalctl

                  Incorrect:
                  systemctl list-units --type=service
                  ip addr show
                  ss -tulpn
                  journalctl -xe

                - Maximum 5 executable names.
                - One executable name per line.
                - No explanations.
                - No numbering.
                - No markdown.
            """
        )
        cache_key = normalize(context)
        cache = load_cache()
        match = get_close_matches(cache_key, cache.keys(), n=1, cutoff=0.7)

        if match:
            logging.info("Cache hit for '%s'\n", match[0])
            return cache[match[0]]
            
        logging.info("Cache miss for '%s'. Fetching commands from Gemini...\n", cache_key)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        if not response.text:
            raise ValueError("Received empty response from API")
        
        cache[cache_key] = response.text.strip().splitlines()
        save_cache(cache)
        
        logging.info("Saved %d commands to cache.\n", len(cache[cache_key]))
        return cache[cache_key]
    
    except httpx.ConnectError:
        logging.error("No internet connection.")
        return []

    except APIError as e:
        logging.error(f"Gemini API error: {e}")
        return []

    except Exception:
        logging.exception("Unexpected error")
        return []