from distutils.log import debug
import string
from flask import Flask, render_template, request
from transformers import (
    AutoTokenizer,
    pipeline,
    AutoModelForSeq2SeqLM

)
app = Flask(__name__)

tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
model = AutoModelForSeq2SeqLM.from_pretrained("distilgpt2")
writer = pipeline("text-generation", model=model, tokenizer=tokenizer, num_return_sequences=3);
@app.route('/', methods=['GET', 'POST'])
def home():
    choice:int = 1;
    if request.method == 'POST':
        if request.form.get('1') is not None:
            choice = 1
        if request.form.get('2') is not None:
            choice = 2
        if request.form.get('3') is not None:
            choice = 3
        input = request.form['name']
        return render_template("index.html", output_text=getArticle(input, choice))
    return render_template("index.html", output_text="")

def getArticle(article:string, index:int) -> string:
    output_text = writer(article, do_sample=False);
    return output_text[index]["generated_text"]
    
if (__name__ == "__main__"):
    app.run(host="0.0.0.0", port=81)
