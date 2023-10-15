# ai-text-summarization

# Description
This project will use a pipeline from Hugging Face to summarize content from a webpage.

# Technical Process
The application will use the beautiful soup library to target all h1, h2, h3 and p tags and get their text values. We will then preprocess the text by segmenting it into chunks of text that can be summarized by the hugging face pipeline. We will then take all the summaries and combine them into one large summary and return it to the user.

# How to run
This program uses pipenv to manage all of the different packages and requirements for this project.
In order to run this program you need to have Python and Pip installed on your machine.
If pipenv is not yet installed please run the following command:
```shell
pip install pipenv
```
Next simply run the following:
```shell
pipenv install
```
This will install of the dependencies.
To run the project update the url variable, or keep the default I have included. Next run the following:
```shell
pipenv shell
```
This will open up the virtual environment that has all dependencies installed. Next just run
```shell
python summary.py
```
Tis will present you with summarized text.

#TODO
I will need to add some logic in place to clean up sentences that either don't make sense, or have imperfect punctuation.
