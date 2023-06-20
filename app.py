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


def fetch_file_by_id(id_num):
    blogs = file()
    id_numbers = [str(blog_id['id']) for blog_id in blogs]
    if id_num not in id_numbers:
        return False
    else:
        return True


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


@app.route('/update/{{ blog["id"] }}', methods=['GET', 'POST'])
def show_form():
    return render_template('update.html')

@app.route('/update/<post_id>', methods=['GET', 'POST'])
def update_form(post_id):
    post = (fetch_file_by_id(post_id))
    if post is False:
        # Post not found
        return "Post not found", 404

    elif request.method == 'POST':

        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')
        id_num = post_id
        new_post = {"id": id_num, "author": author, "title": title, "content": content}
        with open('blog_data.json', 'r') as fileobj:
            current_data = json.load(fileobj)

        current_data.append(new_post)

        with open('blog_data.json', 'w') as fileobj:
            json.dump(current_data, fileobj)
        return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run()
    # print(file())
    # print(fetch_file_by_id(10))
