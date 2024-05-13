class ModelAdapter:
    def __init__(self, model, model_name):
        self.model = model
        self.model_name = model_name

    def create_completion(self, messages):
        return self.model.chat.completions.create(
            messages=messages,
            model=self.model_name,
        )
