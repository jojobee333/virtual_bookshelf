from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)


# create database

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books.db"
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    return render_template("index.html", books=all_books)



@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_book = Book(
        title = request.form.get("name"),
        author = request.form.get("author"),
        rating = request.form.get("rating")
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html")

@app.route("/delete/<int:book_id>")
def delete(book_id):
    book_to_delete = Book.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/edit_rating/<int:id>', methods=['GET', 'POST'])
def edit(id):
    selected_book = Book.query.get(id)
    if request.method == 'POST':
        selected_book.rating = request.form['new-rating']
        db.session.commit()

    return render_template("edit.html", book=selected_book,  id=id)


if __name__ == "__main__":
    app.run(debug=True)

