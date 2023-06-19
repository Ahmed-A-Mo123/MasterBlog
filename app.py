from flask import Flask, render_template, request, url_for, redirect
import json
import random

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    with open('blog_data.json', 'r') as fileobj:
        data = json.load(fileobj)
    return render_template('index.html', posts=data)


def file():
    with open('blog_data.json', 'r') as fileobj:
        current_data = json.load(fileobj)

    return current_data


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')
        id_num = random.randint(4, 100)
        new_post = {"id": id_num, "author": author, "title": title, "content": content}
        with open('blog_data.json', 'r') as fileobj:
            current_data = json.load(fileobj)

        current_data.append(new_post)

        with open('blog_data.json', 'w') as fileobj:
            json.dump(current_data, fileobj)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    # Perform the delete operation using the post_id

    # Example code:
    # Assuming you have a database or data structure that stores the blog posts,
    # you can delete the blog post with the given post_id from the data source.
    # Here's an example assuming you have a list called "posts":
    blog_posts = file()
    for blog in blog_posts:
        if blog['id'] == post_id:
            blog_posts.remove(blog)
        with open('blog_data.json', 'w') as fileobj:
            json.dump(blog_posts, fileobj)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
    # print(file())
