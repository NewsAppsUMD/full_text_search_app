import os
from peewee import *
from playhouse.sqlite_ext import *
from flask import Flask, render_template, request, flash, redirect, url_for

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
        options = {'tokenize': 'porter', 'content': Minute.text}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_term = request.form['search_term']
        results = (Minute.select(Minute, MinuteIndex.rank()).join(MinuteIndex,on=(Minute.id == MinuteIndex.rowid)).where(MinuteIndex.match(search_term)).order_by(MinuteIndex.rank()))
        document_count = len(list(set([x.url for x in results])))
        if document_count > 0:
            recent = results.order_by(Minute.date.desc()).get()
        else:
            recent = Minute.select().order_by(Minute.date.desc()).get()
    else:
        results = None
        search_term = None
        document_count = Minute.select().count()
        recent = Minute.select().order_by(Minute.date.desc()).get()
    return render_template('index.html', results = results, document_count=document_count, search_term = search_term, recent=recent)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)