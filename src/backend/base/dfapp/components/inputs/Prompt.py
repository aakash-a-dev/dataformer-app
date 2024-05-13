from dfapp.field_typing import Prompt, TemplateField, Text
from dfapp.interface.custom.custom_component import CustomComponent


class PromptComponent(CustomComponent):
    display_name: str = "Prompt"
    description: str = "Create a prompt template with dynamic variables."
    icon = "prompts"

    def build_config(self):
        return {
            "template": TemplateField(display_name="Template"),
            "code": TemplateField(advanced=True),
        }

    def build(
        self,
        template: Prompt,
        **kwargs,
    ) -> Text:
        from dfapp.base.prompts.utils import dict_values_to_string

        
        kwargs = dict_values_to_string(kwargs)
        kwargs = {k: "\n".join(v) if isinstance(v, list) else v for k, v in kwargs.items()}
        formatted_prompt = template
        self.status = f'Prompt:\n"{formatted_prompt}"'
        return formatted_prompt
