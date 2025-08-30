from flask import Flask, render_template
import json

with open ("data.json", encoding="utf-8") as file:
    data = json.load(file)

app = Flask(__name__)

@app.route('/')
def index():
    blog_posts = []
    for element in data:
        blog_posts.append(element["content"])
    return render_template('index.html', posts=blog_posts)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
