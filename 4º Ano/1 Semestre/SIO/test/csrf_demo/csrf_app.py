from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def csrf():
	return render_template('csrf.html')

if __name__=='__main__':
	app.run(port=5001) # diferent port
