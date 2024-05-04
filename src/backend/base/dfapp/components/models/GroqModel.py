from dfapp.interface.custom.custom_component import CustomComponent
from groq import Groq
from dfapp.base.models.model import ModelAdapter

class GroqModel(CustomComponent):

    display_name = "Groq Model"
    description = "Generate responses using Groq model and output a new DatasetDict."

    def build_config(self):
        return {
            "api_key": {"display_name": "Groq API Key", "type": "password", "required": True}
        }

    def build(self, api_key: str) -> ModelAdapter:

        self.client = Groq(api_key=api_key)
        model = ModelAdapter(self.client, "mixtral-8x7b-32768")
        return model
