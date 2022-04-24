from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def helloworld():
	return render_template("home.html", body="Custom body")

@app.route("/login")
def login():
        return render_template("login.html")

if __name__ == "__main__":
	app.run(host='0.0.0.0',debug=True)
