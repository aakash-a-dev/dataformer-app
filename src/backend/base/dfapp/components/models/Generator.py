from dfapp.interface.custom.custom_component import CustomComponent
from typing import Optional, Union
from dfapp.base.models.model import ModelAdapter

class Generator(CustomComponent):
    display_name = "Generator"
    description = "Generate responses using Groq model and output a new DatasetDict."

    # def build_config(self):
    #     return {
    #         "groq_api_key": {"display_name": "Groq API Key", "password": True, "info": "API key for accessing Groq services.", "required": True}
    #     }

    def build(self, text:str, model_component: ModelAdapter) -> str:

        chat_completion = model_component.create_completion(
            messages=[{"role": "user", "content": text}]
            )
        response = chat_completion.choices[0].message.content

        return response
