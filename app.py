from flask import Flask, request, render_template, redirect, url_for
import json

with open("data.json", encoding="utf-8") as file:
    data = json.load(file)

app = Flask(__name__)

@app.route('/')
def index():
    posts = []
    for element in data:
        posts.append(element["content"])
    return render_template('index.html', posts=data)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form["title"]
        author = request.form["author"]
        content = request.form["content"]

        new_element = {"id": len(data) + 1,
                    "title": title,
                    "author": author,
                    "content": content}
        data.append(new_element)

        with open("data.json", "w", encoding="utf-8") as filehandle:
            json.dump(data, filehandle, indent=2)
        return redirect(url_for("index"))

    return render_template('add.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
