from transformers import pipeline

class TextGenerator:
    def __init__(self):
        self.text = ""
        self.error = None
        self.pipeline = pipeline('text-generation')

    def set_text(self, text: str) -> None:
        self.text = text

    def generate(self) -> str:
        try:
            output = self.pipeline(
                self.text,
                do_sample=False,
                # temperature=0.2, # can only be set when do_sample=True
                min_length=200,
                max_length=1000,
                no_repeat_ngram_size=2,
            )
            return output[0]['generated_text']
        
        except Exception as e:
            self.error = str(e)
            return ""

if __name__ == "__main__":
    text = "sample_text_here"
    generator = TextGenerator()
    generator.set_text(text)
    generated_text = generator.generate()

    if generator.error:
        print(f"Error: {generator.error}")
    else:
        print("Generated Text:")
        print(generated_text)