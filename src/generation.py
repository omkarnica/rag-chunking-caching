"""
LLM generation module.

This file sends retrieved context + query to the Grok model
using the xAI API. The API is OpenAI-compatible but uses a
different base URL and API key.
"""

import os
from openai import OpenAI


class Generator:

    def __init__(self, config):
        """
        Initialize the LLM client.
        """

        # model name defined in config.yaml
        self.model_name = config["models"]["llm_model"]

        # create xAI client
        self.client = OpenAI(
            api_key=os.getenv("GROK_API_KEY"),
            base_url="https://api.x.ai/v1"
        )

    def generate(self, query, contexts):
        """
        Generate answer using retrieved context.
        """

        # combine parent chunks
        context_text = "\n\n".join(contexts)

        prompt = f"""
You are a helpful assistant answering questions using the provided context.

Context:
{context_text}

Question:
{query}

Instructions:
- Answer using the context above
- If the answer is not present, say you do not know
"""

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        answer = response.choices[0].message.content

        return answer