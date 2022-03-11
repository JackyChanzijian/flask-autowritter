from distutils.log import debug
import string
from flask import Flask, render_template, request
from transformers import (
    AutoTokenizer,
    pipeline,
    AutoModelForSeq2SeqLM

)
app = Flask(__name__)

tokenizer = AutoTokenizer.from_pretrained("cnicu/t5-small-booksum")
model = AutoModelForSeq2SeqLM.from_pretrained("cnicu/t5-small-booksum")
summarizer = pipeline("summarization", model=model, tokenizer=tokenizer);
article = """
Happy womens day to all the females in this comment section!

Also once again loved your video mysticat, keep growing your channel with your amazing content, I have a suggestion, can you make these cursed things into a datapack, like just run one command and see the magic happening and armor stands spawning!, you could even customise it for all shapes, like you accidentally did for the hexagon!
I would really love to try the circle and this triangle, and even the shark, but Im too dumb too successfully copy you lol
"""
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        input = request.form['name']
        return render_template("index.html", summary=getSummary(input))
    return render_template("index.html", summary="")

@app.route("/<article>")
def summary_page(article):
    return getSummary(article)

def getSummary(article:string) -> string:
    summary = summarizer(article, do_sample=False);
    return summary[0]["summary_text"]
    
if (__name__ == "__main__"):
    app.run(host="0.0.0.0", port=80)
