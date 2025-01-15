import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Replace with your actual DeepSeek API endpoint and API key
DEEPSEEK_API_URL = "https://api.deepseek.com/v3/completions"
API_KEY = os.getenv('DEEPSEEK_API_KEY')

def call_deepseek_api(prompt, max_tokens=250, temperature=0.4):
    """
    Calls the DeepSeek v3 API with a given prompt and returns the generated response in JSON format.

    Args:
        prompt (str): The input prompt for the API.
        max_tokens (int): The maximum number of tokens to generate.
        temperature (float): Controls the randomness of the output (lower = more deterministic).

    Returns:
        dict: The API response in JSON format.
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "response_format": "json"  # Ensure the output is in JSON format
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()  # Return the API response as a JSON object

    except requests.exceptions.RequestException as e:
        return {"error": f"Error calling DeepSeek API: {e}"}

def generate_custom_prompt(character):
    """
    Generates a custom prompt for the DeepSeek API based on your template.

    Args:
        character (str): The Chinese character to query.

    Returns:
        str: A formatted prompt for the API.
    """
    prompt = f"""
    You are an expert in Chinese language. 
    Generate a holistic view on the Chinese character '{character}' 
    in terms of the following attributes:

    1. 含义 (meaning): Explain its meaning.
    2. 字形 (character structure): Describe its structure.
    3. 读音 (pronunciation): Provide its pronunciation.
    4. 字源 (etymology): Explain its origin.
    5. 含此字的字 (composite characters): List characters that contain '{character}'.
    6. 同音字 (homophone characters): List other characters that sound like '{character}'.
    7. 常用词组 (common phrases): Provide common phrases containing '{character}' (often 2-characters).
    8. 成语 (idioms): List idioms containing '{character}' (often 4-characters).
    9. 例句 (example sentences): Provide example short sentences or famous quotes using '{character}'.
    10. 短故事 (short stories): Share 1-2 short stories related to '{character}'.
    11. 诗词 (poetry): Include 1-2 famous poems containing and describing '{character}'.
    12. 图片 (images): Suggest simple images illustrating '{character}'.
    13. 音频 (audio): Suggest short audio clips illustrating '{character}'.
    14. 视频 (video): Suggest short video clips illustrating '{character}'.
    15. 电影 (movies): List famous movies related to '{character}' or movie titles containing '{character}'.
    16. 参考资料 (references): Provide additional popular reference materials.
    17. 有趣网站 (interesting websites): Suggest popular websites related to '{character}'.

    Format the output as a valid JSON object.
    """
    return prompt.strip()

def main():
    # Example usage
    character = "人"
    prompt = generate_custom_prompt(character)

    print(f"Generated Prompt:\n{prompt}\n")

    # Call the DeepSeek API
    response = call_deepseek_api(prompt)
    json_out = json.dumps(response, indent=2, ensure_ascii=False)
    print("API Response (JSON):")
    file_json = f"{character}-1.json"
    print(json_out)
    with open(file_json, "w", encoding="utf-8") as f:
        f.write(json_out)

if __name__ == "__main__":
    main()