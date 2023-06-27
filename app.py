from flask import Flask, render_template, request, url_for, redirect
import json
import random

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    """
    Renders the index.html template and displays the blog posts.

    Returns:
        A rendered template with the blog posts.
    """
    with open('blog_data.json', 'r') as fileobj:
        data = json.load(fileobj)
    return render_template('index.html', posts=data)


def file():
    """
    Reads the blog_data.json file and returns its content.

    Returns:
        The content of the blog_data.json file.
    """
    with open('blog_data.json', 'r') as fileobj:
        current_data = json.load(fileobj)

    return current_data


def fetch_file_by_id(id_num):
    """
    Retrieves a blog post from the blog_data.json file by its ID.

    Args:
        id_num (int): The ID of the blog post.

    Returns:
        The blog post with the given ID if found, otherwise None.
    """
    blogs = file()
    id_numbers = [int(blog_id['id']) for blog_id in blogs]
    post = [post for post in blogs if post['id'] == id_num]

    if id_num not in id_numbers:
        return None
    else:
        return post


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Adds a new blog post.

    Returns:
        If the request method is POST, it adds the new post to the blog_data.json file
        and redirects to the index page. Otherwise, it renders the add.html template.
    """
    data = file()
    if request.method == "POST":
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')
        id_num = data[-1]['id'] + 1
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
    """
    Deletes a blog post with the given ID.

    Args:
        post_id (int): The ID of the blog post to be deleted.

    Returns:
        Redirects to the index page after deleting the blog post.
    """
    blog_posts = file()
    for blog in blog_posts:
        if blog['id'] == post_id:
            blog_posts.remove(blog)
        with open('blog_data.json', 'w') as fileobj:
            json.dump(blog_posts, fileobj)
    return redirect(url_for('index'))


@app.route('/update/<post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Updates a blog post with the given ID.

    Args:
        post_id (str): The ID of the blog post to be updated.

    Returns:
        If the request method is POST, it updates the blog post in the blog_data.json file
        and redirects to the index page. Otherwise, it renders the update.html template
        with the blog post to be updated.
    """
    posts = fetch_file_by_id(int(post_id))
    if posts is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        # Step 1: Read the JSON file
        with open('blog_data.json', 'r') as fileobj:
            data = json.load(fileobj)

        # Step 2: Find the dictionary to update
        index_to_update = int(post_id) - 1   # Index of the dictionary you want to update
        dict_to_update = data[index_to_update]

        # Step 3: Modify the dictionary
        dict_to_update['title'] = request.form.get('title')
        dict_to_update['author'] = request.form.get('author')
        dict_to_update['content'] = request.form.get('content')

        # Step 4: Write the updated data structure back to the JSON file
        with open('blog_data.json', 'w') as fileobj:
            json.dump(data, fileobj)
        return render_template('index.html', posts=data)
    else:
        return render_template('update.html', post=posts, id=post_id)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
