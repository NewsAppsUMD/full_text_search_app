from io import BytesIO
import requests
from bs4 import BeautifulSoup
from dateutil.parser import *
import pdfplumber
from playhouse.sqlite_ext import *
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

db.create_tables([Minute, MinuteIndex])

base_url = "https://ethics.maryland.gov/meeting-minutes/?wpfb_list_page="

for page in range(1,9):
    url = base_url + str(page)
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    pdf_links = [x for x in soup.find_all('p') if x.find('a')]
    for link in pdf_links:
        date = parse(link.text.strip())
        pdf_url = link.find('a')['href']
        name = pdf_url.split('/')[-1].replace('.pdf','')
        pdf = requests.get(pdf_url)
        with pdfplumber.open(BytesIO(pdf.content)) as pdf:
            all_pages_text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                all_pages_text += "\n" + page_text if page_text else ""
        Minute.create(date=date, file=name, url=pdf_url, text=all_pages_text)

MinuteIndex.rebuild()
MinuteIndex.optimize()