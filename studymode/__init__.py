from flask import Flask, render_template

app = Flask(__name__)

posts = [
    {
        'author': 'ur mom',
        'title': "how u doing",
        'content': 'good shit'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html')


from studymode import routes
