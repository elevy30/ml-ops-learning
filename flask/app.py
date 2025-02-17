import os
import logging.config
from flask import Flask, render_template,request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def hello():
    return "<HTML><H1> Hello, World! this is a dynamic refresh with debug=True</H1></HTML>"

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        return f'Hello {name}, your email is {str(email)}'
    return render_template('form.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        return f'Hello {name}, your email is {str(email)}'
    return render_template('form.html')

##Variable rule
@app.route('/results/<int:score>')
def show_score(score):
    res = ""
    if score < 50:
        res = 'FAILED' 
    else:
        res = 'PASSED' 

    exp = {'score':score, 'result':res}
    return render_template('result.html', results = exp, score = score)


##if condition  
@app.route('/scores', methods = ['POST', 'GET'])
def insertscore():
    total_score = 0
    if request.method == 'POST':
        math = request.form['math']
        science = request.form['science']
        history = request.form['history']
        english = request.form['english']
        total_score = (int(math) + int(science) + int(history) + int(english))/4
    else:
        return render_template("form_scores.html")

    return redirect(url_for("show_score",score = total_score))

# Main script
if __name__ == '__main__':
    logging.config.fileConfig('logger/logging.conf')
    logger = logging.getLogger(__name__)
    logger.info('Main module started')
    app.run(debug=True)

