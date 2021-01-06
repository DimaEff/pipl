from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required

from app import app, db
from app.forms import LoginForm, RegisterForm
from app.models import User, Post


@app.route('/')
@app.route('/index')
def index():
    users = User.query.all()

    return render_template('news(b5).html', title='news', users=users)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(User.email==form.email_phone.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid email/phone or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))

    return render_template('login(b5).html', title='pipin', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegisterForm()

    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            phone=form.phone.data
        )
        user.set_password(form.password1.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulation! You are now a registered user!')
        return redirect(url_for('index'))

    return render_template('register.html', title='Register', form=form)


@app.route('/profile/<id>', methods=['GET', 'POST'])
def profile(id):
    user = User.query.get_or_404(int(id))
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POST_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=posts.next_num)\
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prevnum)\
        if posts.has_prev else None

    return render_template('profile.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@app.route('/edit_profile/<id>')
def edit_profile(username):
    pass


@app.route('/follow/<id>', methods=['GET', 'POST'])
def follow(id):
    user = User.query.get_or_404(int(id))
    if user is None:
        flash('User {} not found'.format(user.username))
        return redirect('index')
    if user == current_user:
        flash('You cant follow yourself')
        return redirect('index')

    current_user.follow(user)
    db.session.commit()
    flash('You are following {}'.format(user.username))

    return render_template('profile.html', user=user)


@app.route('/unfollow/<id>', methods=['GET', 'POST'])
def unfollow(id):
    user = User.query.get_or_404(int(id))
    if user is None:
        flash('User {} not found'.format(user.username))
        return redirect('index')
    if user == current_user:
        flash('You cant unfollow yourself')
        return redirect('index')

    current_user.unfollow(user)
    db.session.commit()
    flash('You are unfollowing {}'.format(user.username))

    return render_template('profile.html', user=user)

# @app.route('/test', methods=['GET', 'POST'])
# def test():
#     return render_template('test.html')