from cs50 import SQL
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort


app = Flask(__name__)
db = SQL("sqlite:///database.db")

def get_post(post_id):
    post = db.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    db.close()
    if post is None:
        abort(404)
    return post


@app.route('/')
def index():
    posts = db.execute('SELECT * FROM posts').fetchall()
    return render_template('index.html', posts=posts)


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            db.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            db.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    db.execute('DELETE FROM posts WHERE id = ?', (id,))
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))
