from flask import Flask, render_template
import sys

app = Flask(__name__)

@app.route('/')
def homepage():
    #return "Hi there, how ya doin?"
    #return render_template("main.html")
    return render_template("login.html")
	#return render_template("menu1.html")

	
@app.route('/main')
def main():
    #return "Hi there, how ya doin?"
    return render_template("main.html")
    # return render_template("login.html")
	# return render_template("menu1.html")

@app.route('/menu')
def menu1():
    #return "Hi there, how ya doin?"
    #return render_template("main.html")
    # return render_template("login.html")
	return render_template("menu1.html")

#@app.route('/')
#def homepage():
#    #return "Hi there, how ya doin?"
#    #return render_template("main.html")
#    # return render_template("login.html")
#	return render_template("menu1.html")
	

if __name__ == "__main__":
    app.run()
