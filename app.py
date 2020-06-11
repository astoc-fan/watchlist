# import os
# import sys
#
# import click
# from flask import Flask, render_template, request, url_for, redirect, flash
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
# from werkzeug.security import generate_password_hash, check_password_hash
#
# # SQLite URI compatible
# WIN = sys.platform.startswith('win')
# if WIN:
#     prefix = 'sqlite:///'
# else:
#     prefix = 'sqlite:////'
#
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'dev'
# app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# db = SQLAlchemy(app)
# login_manager = LoginManager(app)
#
#
# @login_manager.user_loader
# def load_user(user_id):
#     user = User.query.get(int(user_id))
#     return user
#
#
# login_manager.login_view = 'login'
#
#
# # login_manager.login_message = 'Your custom message'
#
#
#
#
#
# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(20))
#     username = db.Column(db.String(20))
#     password_hash = db.Column(db.String(128))
#
#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)
#
#     def validate_password(self, password):
#         return check_password_hash(self.password_hash, password)
#
#
# class Movie(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(60))
#     year = db.Column(db.String(4))
#
#
# @app.context_processor
# def inject_user():
#     user = User.query.first()
#     return dict(user=user)
#
#
# @app.errorhandler(400)
# def bad_request(e):
#     return render_template('400.html'), 400
#
#
# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404
#
#
# @app.errorhandler(500)
# def internal_server_error(e):
#     return render_template('500.html'), 500
#
#
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         if not current_user.is_authenticated:
#             return redirect(url_for('index'))
#
#         title = request.form['title']
#         year = request.form['year']
#
#         if not title or not year or len(year) > 4 or len(title) > 60:
#             flash('Invalid input.')
#             return redirect(url_for('index'))
#
#         movie = Movie(title=title, year=year)
#         db.session.add(movie)
#         db.session.commit()
#         flash('Item created.')
#         return redirect(url_for('index'))
#
#     movies = Movie.query.all()
#     return render_template('index.html', movies=movies)
#
#
# @app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
# @login_required
# def edit(movie_id):
#     movie = Movie.query.get_or_404(movie_id)
#
#     if request.method == 'POST':
#         title = request.form['title']
#         year = request.form['year']
#
#         if not title or not year or len(year) > 4 or len(title) > 60:
#             flash('Invalid input.')
#             return redirect(url_for('edit', movie_id=movie_id))
#
#         movie.title = title
#         movie.year = year
#         db.session.commit()
#         flash('Item updated.')
#         return redirect(url_for('index'))
#
#     return render_template('edit.html', movie=movie)
#
#
# @app.route('/movie/delete/<int:movie_id>', methods=['POST'])
# @login_required
# def delete(movie_id):
#     movie = Movie.query.get_or_404(movie_id)
#     db.session.delete(movie)
#     db.session.commit()
#     flash('Item deleted.')
#     return redirect(url_for('index'))
#
#
# @app.route('/settings', methods=['GET', 'POST'])
# @login_required
# def settings():
#     if request.method == 'POST':
#         name = request.form['name']
#
#         if not name or len(name) > 20:
#             flash('Invalid input.')
#             return redirect(url_for('settings'))
#
#         user = User.query.first()
#         user.name = name
#         db.session.commit()
#         flash('Settings updated.')
#         return redirect(url_for('index'))
#
#     return render_template('settings.html')
#
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#
#         if not username or not password:
#             flash('Invalid input.')
#             return redirect(url_for('login'))
#
#         user = User.query.first()
#
#         if username == user.username and user.validate_password(password):
#             login_user(user)
#             flash('Login success.')
#             return redirect(url_for('index'))
#
#         flash('Invalid username or password.')
#         return redirect(url_for('login'))
#
#     return render_template('login.html')
#
#
# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     flash('Goodbye.')
#     return redirect(url_for('index'))
