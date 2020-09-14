from flask import Flask, render_template,session,redirect
from flask_sqlalchemy import SQLAlchemy
from flask import request
import json
import os
import math
from flask_mail import Mail
from datetime import datetime
from werkzeug.utils import secure_filename


with open('config.json','r') as c:
    params = json.load(c)["params"]


app = Flask(__name__)
app.secret_key = 'super-secret-key'
app.config['UPLOAD_FOLDER'] = params['file_location']
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD = params['gmail-pass']
)
mail = Mail(app)


local_server = True
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)

class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.Integer, unique=True, nullable=False)
    msg = db.Column(db.String(120), unique= False, nullable=False)


class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    content = db.Column(db.String(120), unique=True, nullable=False)
    date = db.Column(db.String(120), unique= False, nullable=False)
    img_file = db.Column(db.String(120), unique= False, nullable=False)
class Array(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    content = db.Column(db.String(120), unique=True, nullable=False)
    date = db.Column(db.String(120), unique= False, nullable=False)


@app.route('/ds')
def ds():
    posts = Posts.query.filter_by().all()
    return render_template('ds.html', posts = posts)

# all endpoint for data structures
@app.route('/array')
def array():
    posts = Array.query.filter_by().all()
    return render_template('array.html', posts = posts)

@app.route('/Linked-list')
def linked():
    posts = Posts.query.filter_by().all()
    return render_template('linkedlist.html', posts = posts)
@app.route('/Stack')
def stack():
    posts = Posts.query.filter_by().all()
    return render_template('stack.html', posts = posts)







@app.route('/algo')
def algo():
    return render_template('algo.html')

@app.route('/')
def home():
    posts = Posts.query.filter_by().all()
    last = math.ceil(len(posts) / int(params['no_of_post']))
    page = request.args.get('page', type = int)
    if (not str(page).isnumeric()):
        page = 1
    #page = int(page)
    posts = posts[(page - 1) * int(params['no_of_post']):(page - 1) * int(params['no_of_post']) + int(params['no_of_post'])]
    if page == 1:
        prev = "#"
        next = "/?page=" + str(page + 1)
    elif page == last:
        prev = "/?page=" + str(page - 1)
        next = "#"
    else:
        prev = "/?page=" + str(page - 1)
        next = "/?page=" + str(page + 1)
    # posts = Posts.query.filter_by().all()[0:params['no_of_post']]
    return render_template('index.html', params=params, posts=posts, prev=prev, next=next)


@app.route('/index')
def index():
    posts = Posts.query.filter_by().all()
    last = math.ceil(len(posts)/int(params['no_of_post']))
    page = request.args.get('page')
    if(not str(page).isnumeric()):
        page = 1
    posts = posts[(page-1)*int(params['no_of_post']):(page-1)*int(params['no_of_post'])+ int(params['no_of_post'])]
    if page == 1:
        prev = "#"
        next = "/?page=" + str(page + 1)
    elif page == last:
        prev = "/?page=" + str(page - 1)
        next = "#"
    else:
        prev = "/?page=" + str(page - 1)
        next = "/?page=" + str(page + 1)
    # posts = Posts.query.filter_by().all()[0:params['no_of_post']]
    return render_template('index.html', params = params,posts = posts,prev = prev,next = next)       #jinjs for loop er jonno posts pathate hobe

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/dashboard')
@app.route('/uploader', methods = ['GET','POST'])
def uploader():
    if ('user' in session and session['user'] == params['admin_user']):
        if(request.method == 'POST'):
            f = request.files['file1']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            return "upload successfully"

@app.route('/delete/<string:sno>', methods =['GET','POST'])
def delete(sno):
    if('user' in session and session['user'] == params['admin_user']):
        post = Posts.query.filter_by(sno = sno).first()
        db.session.delete(post)
        db.session.commit()
        return redirect('/dashboard')

@app.route('/array/<string:post_slug>',methods = ['GET'])
def array_route(post_slug):
    post = Array.query.filter_by(slug=post_slug).first()
    return render_template('ArrayContent.html',post=post)

@app.route('/edit/array/<string:sno>', methods =['GET','POST'])
def editArray(sno):
    if('user' in session and session['user'] == params['admin_user']):
        if(request.method == 'POST'):
            title = request.form.get('title')
            slug = request.form.get('slug')
            content = request.form.get('content')

            date = datetime.now()
            if(sno == "0"):
                post = Array(title = title, content = content,date = date,slug= slug)
                db.session.add(post)
                db.session.commit()
            else:
                post = Array.query.filter_by(sno=sno).first()
                post.title = title

                post.content = content
                post.date = date

                db.session.commit()
                redirect('/edit/array'+ sno)
        post = Array.query.filter_by(sno=sno).first()
        return render_template('editArray.html',params = params, post = post,sno = sno)


@app.route('/edit/<string:sno>', methods =['GET','POST'])
def edit(sno):
    if('user' in session and session['user'] == params['admin_user']):
        if(request.method == 'POST'):
            title = request.form.get('title')
            slug = request.form.get('slug')
            content = request.form.get('content')
            img_file = request.form.get('img_file')
            date = datetime.now()
            if(sno == "0"):
                post = Posts(title = title,slug = slug, content = content,img_file = img_file,date = date)
                db.session.add(post)
                db.session.commit()
            else:
                post = Posts.query.filter_by(sno=sno).first()
                post.title = title
                post.slug = slug
                post.content = content
                post.date = date
                post.img_file = img_file
                db.session.commit()
                redirect('/edit/'+ sno)
        post = Posts.query.filter_by(sno=sno).first()
        return render_template('edit.html',params = params, post = post,sno = sno)


@app.route('/dashboard', methods = ['GET', 'POST'])
def login():
    if('user' in session and session['user'] == params['admin_user']):
        posts = Posts.query.all()
        return render_template('dashboard.html', params = params,posts = posts)



    if request.method == 'POST':
        username = request.form.get('user')
        userpass = request.form.get('pass')
        if(username == params['admin_user'] and userpass == params['admin_pass']):
            session['user'] = username
            posts = Posts.query.all()
            return render_template('dashboard.html', params = params , posts = posts)


    return render_template('login.html', params = params)

@app.route('/contact', methods = ['GET', 'POST'])
def contact():
    if request.method =='POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone_num')
        msg = request.form.get('msg')
        entry = Contacts(name = name, phone =phone,msg = msg,email = email)
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from' + name,
                            sender = email,
                            recipients = [params['gmail-user']],
                            body = msg + "\n" + phone
                          )
    return render_template('contact.html')

@app.route('/post/<string:post_slug>',methods = ['GET'])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html',post=post)





app.run(debug=True)

