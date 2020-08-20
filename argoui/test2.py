
from flask import Flask, render_template,request

app = Flask(__name__)



@app.route('/')
def hello_world():
    return "ghelo"

@app.route('/hello')
def hello():
    return "ghelo"

if __name__ == '__main__':
    app.run(debug=True,port=9000)
