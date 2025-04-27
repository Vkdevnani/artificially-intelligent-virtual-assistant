import requests

# Replace with your GitHub Copilot API endpoint and API key
api_url = 'https://api.github.com/copilot/complete'
api_key = 'your-github-api-key'


def get_copilot_response(prompt):
    headers = {
        'Authorization': f'token {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'prompt': prompt,
        'model': 'copilot-model',  # Replace with the appropriate model name if required
        'max_tokens': 150  # Adjust based on the expected length of the response
    }

    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        result = response.json()
        return result['choices'][0]['text'].strip()  # Adjust based on the response format
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"


if __name__ == "__main__":
    user_prompt = input("Enter your prompt: ")
    output = get_copilot_response(user_prompt)
    print("Response from GitHub Copilot:")
    print(output)
