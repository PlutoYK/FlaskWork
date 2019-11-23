from app import app
from flask import redirect,render_template,flash,url_for,request,g
from app.forms import LoginForm,RegistrationForm,EditProfileForm,PostForm,ResetPasswordRequestForm,ResetPasswordForm
from flask_login import current_user,login_user,login_required,logout_user
from app.models import  User,Post
from app import  db
from datetime import datetime
from werkzeug.urls import  url_parse
from app.email import send_password_reset_email

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()





# 主页函数

@app.route('/index',methods=['POST','GET'])
@app.route('/', methods=['POST', 'GET'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body = form.posts.data,author= current_user )
        db.session.add(post)
        db.session.commit()
        flash('your post is now live')
        return redirect(url_for('index'))

    page = request.args.get('page',1,type = int)
    posts = current_user.followed_posts().paginate(page,app.config['POSTS_PER_PAGE'],False)
    next_url = url_for('index',page = posts.next_num)\
    if posts.has_next else None
    prev_url = url_for('index',page = posts.prev_num)\
    if posts.has_prev else None
    return render_template('index.html', title = 'Home page',form = form,posts = posts.items,next_url = next_url,prev_url = prev_url)




# 登陆页面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # flash('Login requested for{},remember_me{}'.format(form.username.data,form.remember_me.data))
        user = User.query.filter_by(username = form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user,remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc !='':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title = 'Sign In',form = form)
# 登出页面
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
# 注册页面
@app.route('/register',methods=['POST','GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data,email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations,you are a redistered user now')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form = form)
# 个人用户主页
@login_required
@app.route('/user/<username>')
def user(username):
    user= User.query.filter_by(username = username).first_or_404()
    # posts = [
    #     {'author': user, 'body': 'Test post #1'},
    #     {'author': user, 'body': 'Test post #2'}
    # ]
    page = request.args.get('page',1,type = int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(page,app.config['POSTS_PER_PAGE'],False)
    next_url = url_for('user',username = user.username,page = posts.next_num)\
    if posts.has_next else None
    prev_url = url_for('user',username = user.username,page = posts.prev_num)\
    if posts.has_prev else None
    return render_template('user.html',user= user,posts =  posts.items,next_url = next_url,prev_url = prev_url)


# 个人信息编辑
@app.route('/editProfile',methods=['GET','POST'])
@login_required
def editProfile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('your changes have saved successfully! ')
        return redirect(url_for('editProfile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('editProfile.html',title = 'Edit Profile',form = form)
# 关注用户
@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username = username).first()
    if user is None:
        flash('user {}not found'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('you cannot follow yourself')
        return redirect(url_for('user',username= username))
    current_user.follow(user)
    db.session.commit()
    flash('you have followed {} successfully'.format(username))
    return redirect(url_for('user',username= username))
# 取消关注
@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username =username).first()
    if user is None:
        flash('{} is not found'.format(username))
        return redirect(url_for('index'))
    if username ==current_user:
        flash('you can\'t unfollow yourself')
        return redirect(url_for('user',username = username))
    current_user.unfollow(user)
    db.session.commit()
    flash('you have unfollowed {}'.format(username))
    return redirect(url_for('user',username = username))
# 发现新的用户
@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page',1,type = int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page,app.config['POSTS_PER_PAGE'],False)
    next_url = url_for('explore',page = posts.next_num)\
    if posts.has_next else None
    prev_url = url_for('explore',page = posts.prev_num) \
    if posts.has_prev else None
    return render_template('index.html',title = 'Explore',posts = posts.items,next_url = next_url,prev_url = prev_url)

# 重置密码表单提交
@app.route('/reset_password_request',methods=['POST','GET'])
def reset_password_request():
    form = ResetPasswordRequestForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('resetPasswordRequest.html',title = 'Reset Password',form = form)


@app.route('/reset_password/<token>',methods=['POST','GET'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has reset.')
        return redirect(url_for('login'))
    return render_template('resetpassword.html',form = form)



@app.route('/user/<username>/popup')
@login_required
def user_popup(username):
    user = User.query.filter_by(username = username).first_or_404()
    return render_template('user_popup.html',user = user)