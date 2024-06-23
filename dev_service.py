from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
from transformers import BartTokenizer, BartForConditionalGeneration, pipeline

app = Flask(__name__)

model_name = "./bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)
summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_article', methods=['POST'])
def get_article():
    url = request.form['url']
    max_length = int(request.form.get('max_length', 300))
    min_length = int(request.form.get('min_length', 100))
    article_text = scrape_article(url)
    summary = summarize_text(article_text, max_length, min_length)
    return render_template('index.html', summary=summary, max_length=max_length, min_length=min_length)

def scrape_article(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    article_text = ' '.join([para.get_text() for para in paragraphs])
    return article_text

def summarize_text(text, max_length, min_length):
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text']
    return summary

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
