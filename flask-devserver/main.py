from flask import Flask, redirect, render_template
import liveserver
app = Flask(__name__)

@app.route('/')
def landing():
    return render_template("index.html")

@app.route('/welcome')
def welcome():    
    return redirect("http://localhost:5500/redirect", code=302)

@app.route('/redirect')
def redirection():    
    return '<h1>Redirection works</h1>'

@app.route('/<name>')
def helloname(name):    
    return '<h1>Hello {0}</h1>'.format(name)

if __name__ == '__main__':    
    liveserver.serve(app)

