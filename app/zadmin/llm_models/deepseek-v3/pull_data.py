import requests
import json

# Replace with your actual DeepSeek API endpoint and API key
DEEPSEEK_API_URL = "https://api.deepseek.com/v3/completions"
API_KEY = "your_deepseek_api_key_here"

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
    You are an expert in Chinese language. Generate a holistic view on the Chinese character '{character}' in terms of the following attributes:

    1. 含义 (meaning): Explain its meaning.
    2. 字形 (character structure): Describe its structure.
    3. 读音 (pronunciation): Provide its pronunciation.
    4. 字源 (etymology): Explain its origin.
    5. 含此字的字 (composite characters): List characters that contain '{character}'.
    6. 常用词组 (common phrases): Provide common phrases containing '{character}'.
    7. 成语 (idioms): List idioms containing '{character}'.
    8. 例句 (example sentences): Provide example sentences using '{character}'.
    9. 短故事 (short stories): Share a short story related to '{character}'.
    10. 诗词 (poetry): Include famous poems containing '{character}'.
    11. 图片 (images): Suggest simple images illustrating '{character}'.
    12. 音频 (audio): Suggest short audio clips illustrating '{character}'.
    13. 视频 (video): Suggest short video clips illustrating '{character}'.
    14. 电影 (movies): List famous movies related to '{character}'.
    15. 参考资料 (references): Provide additional reference materials.
    16. 有趣网站 (interesting websites): Suggest websites related to '{character}'.

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
    print("API Response (JSON):")
    print(json.dumps(response, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()