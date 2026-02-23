import requests
import json
import sys
from pathlib import Path

OLLAMA_URL = "http://localhost:11434/api/generate"

# This script helps you understand how applications "talk" to AI models.
# You will implement a function to send a message to your local Ollama instance.


# Function to send a prompt to the local model
def query_ollama(model_name, prompt_text, timeout=30):
    """
    Args:
        model_name (str): Ollama model tag, e.g. "llama3.2:1b" or "llama3.2:3b"
        prompt_text (str): The user prompt to send to the model
        timeout (int): Request timeout in seconds

    Returns:
        dict: Parsed JSON response from Ollama, or {"error": "..."} on failure
    """
    payload = {
        "model": model_name,
        "prompt": prompt_text,
        "stream": False
    }

    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}
    except json.JSONDecodeError:
        return {"error": "Failed to parse JSON response from Ollama."}


# Function to save the result to a file (for documentation)
def save_result(output_path, model_name, prompt_text, response_text):
    """
    Saves prompt + response to a text file.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    content = (
        f"MODEL: {model_name}\n\n"
        f"PROMPT:\n{prompt_text}\n\n"
        f"RESPONSE:\n{response_text}\n"
    )

    output_path.write_text(content, encoding="utf-8")
    return str(output_path)


# Main execution block
if __name__ == "__main__":

    print("Initializing Local AI Connection...")

    # Choose your local model:
    my_model = "tinyllama"  # fastest
    # my_model = "llama3.2:3b"  # better quality (slower)

    my_prompt = "Why is documentation important? Answer in 3 bullet points."

    result = query_ollama(my_model, my_prompt, timeout=60)

    if result.get("error"):
        print("Error:", result["error"])
        sys.exit(1)

    # Common key for Ollama /api/generate output:
    response_text = result.get("response", "")

    print("\n--- MODEL RESPONSE ---\n")
    print(response_text)

    saved = save_result(
        output_path="outputs/ollama_response.txt",
        model_name=my_model,
        prompt_text=my_prompt,
        response_text=response_text
    )

    print(f"\nSaved to: {saved}")
