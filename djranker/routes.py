from flask import render_template, request
from djranker import app,handlers,word_count
import pandas as pd

WordCounter = word_count.WordCount()
@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        WordCounter.jokes_number = int(request.form['jokes'])
        return table()
    return render_template('home.html')
@app.route('/table', methods=['GET','POST'])
def table():
    if request.method == 'POST':
        for _ in range(WordCounter.jokes_number):
            handlers.get_jokes(WordCounter)
        WordCounter.update_ranks()
    return render_template('table.html',  tables=[WordCounter.df.to_html(classes='data', header="true",index=False)])
    