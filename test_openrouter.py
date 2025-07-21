import requests

url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": "Bearer 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",
    "Content-Type": "application/json"
}

payload = {
    "model": "openai/gpt-3.5-turbo",
    "messages": [
        {"role": "user", "content": "Hello! Can you reply with just the word YES if you received this?"}
    ]
}

response = requests.post(url, headers=headers, json=payload)

print("Status Code:", response.status_code)
print("Response:")
print(response.json())
