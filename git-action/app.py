from flask import Flask

app=Flask(__name__)

@app.route("/")
def home():
    return"Hello World"

if __name__== "__main__":
    print("version 2")
    app.run(debug=True,host='0.0.0.0',port=5001)