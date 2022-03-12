from distutils.log import debug
import string
from flask import Flask, render_template, request
from transformers import (
    AutoTokenizer,
    pipeline,
    AutoModelForCausalLM
)
app = Flask(__name__)

tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
model = AutoModelForCausalLM.from_pretrained("distilgpt2")
writer = pipeline("text-generation", model=model, tokenizer=tokenizer);
@app.route('/', methods=['GET', 'POST'])
def home():
    choice:int = 0
    if request.method == 'POST':
        # if request.form.get('1') is not None:
        #     choice = 1
        # if request.form.get('2') is not None:
        #     choice = 2
        # if request.form.get('3') is not None:
        #     choice = 3
        input = request.form['input']
        return render_template("index.html", output_text=getArticle(input, choice))
    return render_template("index.html", output_text="")

def getArticle(article:string, index:int) -> string:
    encoded_input = tokenizer(article)
    word_count:int = len(encoded_input['input_ids'])
    output_text = writer(article,  min_length=word_count + 10, max_length=word_count + 30)
    print(word_count)
    return output_text[0]["generated_text"]
    
if (__name__ == "__main__"):
    app.run(port=8081)
