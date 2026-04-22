import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

my_endpoint = "https://models.github.ai/inference"
model_name = "mistral-ai/mistral-small-2503"

with open("token.env", "r") as f:
    token = f.read().strip()
if not token:
    raise ValueError("Imposta GITHUB_TOKEN nel file .env")

client = ChatCompletionsClient(
    endpoint=my_endpoint,
    credential=AzureKeyCredential(token),
)

prompt = input("Inserisci il tuo prompt: ")

response = client.complete(
    messages=[
        UserMessage(prompt),
    ],
    temperature=1.0,
    top_p=1.0,
    max_tokens=1000,
    model=model_name
)

print(response.choices[0].message.content)