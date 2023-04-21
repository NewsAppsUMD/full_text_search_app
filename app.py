import os
from peewee import *
from flask import Flask, render_template, request, flash, redirect, url_for
from playhouse.sqlite_ext import *
app = Flask(__name__)
app.secret_key = "e908eh3hiur33jrh3"
db = SqliteExtDatabase('ethics.db')

class Minute(Model):
    date = DateField()
    file = CharField()
    url = CharField()
    text = TextField()

    class Meta:
        table_name = "minutes"
        database = db

class MinuteIndex(FTSModel):
    rowid = RowIDField()
    text = SearchField()

    class Meta:
        database = db
        options = {'tokenize': 'porter'}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        zip_code = request.form['zip_code']
        try:
            zip_code_data = ZipCode.get(ZipCode.zipcode == zip_code)
            return redirect(url_for('detail', slug=zip_code))
        except ZipCode.DoesNotExist:
            flash(f"Zip code {zip_code} not found.", 'error')
    else:
        top_zips = Notice.select().where(Notice.month == '2023-03-01').order_by(Notice.notices.cast('int').desc()).limit(10)
    return render_template('index_new.html', top_zips=top_zips)

@app.route('/zipcode/<slug>')
def detail(slug):
    zipcode = ZipCode.get(ZipCode.zipcode==slug)
    notices = Notice.select().where(Notice.zip==slug)
    total_notices = Notice.select(fn.SUM(Notice.notices).alias('sum')).where(Notice.zip==slug).scalar()
    geojson_url = f"/static/zipcode_{slug}.geojson"
    notice_json = []
    for notice in notices:
        notice_json.append({'x': str(notice.month.year) + ' ' + str(notice.month.month), 'y': notice.zip, 'heat': notice.notices})
    return render_template("detail.html", zipcode=zipcode, notices=notices, notices_count=len(notices), notice_json = notice_json, total_notices = total_notices, geojson_url = geojson_url)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)