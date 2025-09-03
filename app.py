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


@app.route('/delete/<int:post_id>', methods=["GET", "POST"])
def delete(post_id):
    post = None
    for element in data:
        if element.get("id") == post_id:
            post = element
            break
    if not post:
        return redirect(url_for('index'))

    if request.method == "POST":
        data.remove(post)
        with open("data.json", "w", encoding="utf-8") as filehandle:
            json.dump(data, filehandle, indent=2)
        return redirect(url_for('index'))
    return render_template("delete.html", post=post)


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    post = None
    for element in data:
        if element.get("id") == post_id:
            post = element
            break
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        title = request.form.get("title")
        author = request.form.get("author")
        content = request.form.get("content")

        if not title or not author or not content:
            return render_template('update.html', post=post)

        post["title"] = title
        post["author"] = author
        post["content"] = content

        with open("data.json", "w", encoding="utf-8") as filehandle:
            json.dump(data, filehandle, indent=2)
        return redirect(url_for("index"))

    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
