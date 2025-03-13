import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

class AzureGPTClient:
    def __init__(self):
        self.endpoint = os.getenv("ENDPOINT_URL")
        self.deployment = os.getenv("DEPLOYMENT_NAME")
        self.subscription_key = os.getenv("AZURE_OPENAI_API_KEY")
        
        if not all([self.endpoint, self.deployment, self.subscription_key]):
            raise ValueError("Missing required environment variables")
        
        self.client = AzureOpenAI(
            azure_endpoint=self.endpoint,
            api_key=self.subscription_key,
            api_version="2024-05-01-preview",
        )

    def get_completion(self, system_prompt, user_prompt):
        chat_prompt = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": system_prompt
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_prompt
                    }
                ]
            }
        ]

        messages = chat_prompt

        completion = self.client.chat.completions.create(
            model=self.deployment,
            messages=messages,
            max_tokens=4090,
            temperature=0.4,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            stream=False
        )

        return completion.choices[0].message.content

# Example usage
if __name__ == "__main__":
    client = AzureGPTClient()
    result = client.get_completion("You are an AI assistant that helps people find information.", "tell me a joke on pc parts")
    print((result))
