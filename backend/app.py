from flask import Flask, render_template, request
from opensourcefit_ml import analyze_repository

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        repo = request.form["repo"]
        skills = request.form["skills"]
        result = analyze_repository(repo, skills)

    return render_template(
        "index.html",
        repo=repo if request.method == "POST" else "",
        skills=skills if request.method == "POST" else "",
        result=result if request.method == "POST" else None
    )

if __name__ == "__main__":
    app.run(debug=True)