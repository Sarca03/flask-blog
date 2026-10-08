from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from app import db
from app.models import User, Post, Comment
from app.forms import RegistrationForm, LoginForm, PostForm, CommentForm
from flask_login import login_user, current_user, logout_user, login_required

bp = Blueprint('routes', __name__)


@bp.route("/")
@bp.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('index.html', posts=posts)


@bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('routes.home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)

        # Prvi korisnik postaje admin
        if User.query.count() == 0:
            user.is_admin = True

        db.session.add(user)
        db.session.commit()
        flash('Nalog je uspešno kreiran! Sada se možeš prijaviti.', 'success')
        return redirect(url_for('routes.login'))

    return render_template('register.html', title='Registracija', form=form)


@bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f"Uspešno si prijavljen, dobrodošao {user.username}!", 'success')
            return redirect(next_page) if next_page else redirect(url_for('routes.home'))
        else:
            flash('Neuspešna prijava. Proveri email i lozinku.', 'danger')

    return render_template('login.html', title='Prijava', form=form)


@bp.route("/logout")
def logout():
    logout_user()
    flash('Uspešno si se odjavio.', 'info')
    return redirect(url_for('routes.home'))


@bp.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            subtitle=form.subtitle.data,
            content=form.content.data,
            author=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash('Članak je uspešno objavljen!', 'success')
        return redirect(url_for('routes.home'))
    return render_template('create_post.html', title='Novi članak', form=form, legend='Novi blog članak')


@bp.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('Moraš biti prijavljen da bi ostavio komentar.', 'warning')
            return redirect(url_for('routes.login'))

        comment = Comment(content=form.content.data, author=current_user, post=post)
        db.session.add(comment)
        db.session.commit()
        flash('Komentar je uspešno dodat!', 'success')
        return redirect(url_for('routes.post', post_id=post.id))

    return render_template('post.html', title=post.title, post=post, form=form)


@bp.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user and not current_user.is_admin:
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.content = form.content.data
        db.session.commit()
        flash('Članak je uspešno izmenjen!', 'success')
        return redirect(url_for('routes.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.subtitle.data = post.subtitle
        form.content.data = post.content

    return render_template('create_post.html', title='Izmeni članak', form=form, legend='Izmena članka')


@bp.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user and not current_user.is_admin:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('Članak je obrisan.', 'info')
    return redirect(url_for('routes.home'))