# Text Summarization Script using Hugging Face Transformers

from transformers import pipeline
import requests
from bs4 import BeautifulSoup


class TextSummarization:
    def __init__(self):
        self.url = ""
        self.content = ""
        self.error = None
        self.pipeline = pipeline('summarization')


    def set_url(self, url: str) -> None:
        """Set the URL to retrieve content from."""
        self.url = url


    def extract_visible_text(self, html_content: bytes) -> str:
        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all text within the HTML body
        results = soup.find_all(['h1','h2','h3','p'])
        text = [result.text for result in results]

        output = ' '.join(text)

        return output


    def preprocess_text(self, text: str) -> str:
        "Replace punctuation to make preprocessing easier."
        text = text.replace('.', '.<eos>')
        text = text.replace('!', '!<eos>')
        text = text.replace('?', '?<eos>')

        max_chunk = 500
        sentences = text.split('<eos>')
        current_chunk = 0 
        chunks = []

        for sentence in sentences:
            if len(chunks) == current_chunk + 1: 
                if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk:
                    chunks[current_chunk].extend(sentence.split(' '))
                else:
                    current_chunk += 1
                    # print(sentence)
                    chunks.append(sentence.split(' '))
            else:
                # print(current_chunk)
                chunks.append(sentence.split(' '))

        for chunk_id in range(len(chunks)):
            chunks[chunk_id] = ' '.join(chunks[chunk_id])
        # print(chunks)
        return chunks


    def get_content(self) -> None:
        """Retrieve content from the specified URL."""
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                html_content = self.extract_visible_text(response.content)
                self.content = self.preprocess_text(html_content)
            else:
                self.error = f"Failed to retrieve content. Status code: {response.status_code}"
        except requests.RequestException as e:
            self.error = f"Request error: {str(e)}"


    def summarize(self, max_length: int = 50, min_length: int = 30) -> str:
        """Summarize the content."""
        if not self.content:
            self.get_content()
        if self.error:
            return self.error

        result = self.pipeline(
            self.content,
            max_length=max_length,
            min_length=min_length,
            do_sample=False
        )

        output = ' '.join([summary['summary_text'] for summary in result])

        return output


if __name__ == "__main__":
    url="https://www.bairesdev.com/blog/why-is-python-top-language/"
    summarizer = TextSummarization()
    summarizer.set_url(url)
    summary = summarizer.summarize()

    if summarizer.error:
        print(f"Error: {summarizer.error}")
    else:
        print("Summary:")
        print(summary)
