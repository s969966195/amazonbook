#coding=utf-8

from flask import Flask,render_template,request
from flask_script import Manager
from flask_mongoengine import MongoEngine
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,BooleanField
from wtforms.validators import Required
from flask_bootstrap import Bootstrap
import subprocess
import re
import urllib

app=Flask(__name__)
app.config['MONGODB_SETTINGS']={
    'db':'amazon',
    'host':'127.0.0.1',
    'port':27017
}
app.config['SECRET_KEY']='hard to guess string'

manager=Manager(app)
db=MongoEngine(app)
bootstrap=Bootstrap(app)


class Book(db.Document):
    meta={
        'collection':'book',
        'ordering':['-create_at'], #指定顺序
        'strict':False, #是否严格模式
    }
    title=db.StringField(required=True)
    author=db.StringField()
    press=db.StringField()
    ISBN=db.StringField()
    ASIN=db.StringField()
    introduction=db.StringField()
    promotion=db.StringField()
    prime_paperback=db.StringField()
    prime_ebook=db.StringField()

class BookForm(FlaskForm):
    book=StringField(u'需要找什么书?',validators=[Required()])
    submit=SubmitField(u'搜索')
    search=BooleanField(u'在网上搜索')

@app.route('/',methods=['GET','POST'])
def index():
    title=None
    spider_name="amazon"
    form=BookForm()
    if form.validate_on_submit():
        name=form.book.data
        form.book.data=''
        if form.search.data:
            n=name.encode('utf-8')
            s=str(n)
            f={'field-keywords':s}
            params=urllib.urlencode(f)
            subprocess.Popen('scrapy crawl amazon -a start_url="https://www.amazon.cn/s/ref=nb_sb_noss?__mk_zh_CN=%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99&url=search-alias%3Dstripbooks&{0}"'.format(params),shell=True)
        else:
            search={'__raw__':{'title':{'$in':map(re.compile,name.split())}}}
            page=request.args.get('page',1,type=int)
            pagination=Book.objects(**search).all().paginate(page=page,per_page=10)
            books=pagination.items
            return render_template('index.html',form=form,books=books,pagination=pagination)
    page=request.args.get('page',1,type=int)
    pagination=Book.objects.order_by('_published_at').paginate(page=page,per_page=10)
    books=pagination.items
    return render_template('index.html',form=form,books=books,pagination=pagination)

@app.route('/book/<ASIN>')
def book(ASIN):
    book=Book.objects(ASIN=ASIN).first()
    if book is None:
        abort(404)
    return render_template('book.html',book=book)

if __name__=='__main__':
    manager.run()
