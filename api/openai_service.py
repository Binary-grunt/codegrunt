from openai import OpenAI


class OpenAIService:

    DEFAULT_MODEL = "gpt-4o-mini"  # Default model for OpenAI interactions

    def __init__(self, client: OpenAI, model: str = None):
        self.client = client
        self.model = model or self.DEFAULT_MODEL

    def send_message(self, messages: list[dict]) -> str:
        try:
            completion = self.client.chat.completions.create(model=self.model, messages=messages)
            return completion.choices[0].message.content
        except Exception as e:
            raise ValueError(f"Failed to process the request: {e}")
