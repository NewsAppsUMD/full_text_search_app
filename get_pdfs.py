from io import BytesIO
import sqlite3
import requests
from bs4 import BeautifulSoup
from dateutil.parser import *
import pdfplumber
from sqlite_utils import Database

db = Database("ethics.db")
base_url = "https://ethics.maryland.gov/meeting-minutes/?wpfb_list_page="
pdf_list = []

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
        pdf_list.append({"date": date, "file": name, "url": pdf_url, "text": all_pages_text})

db["minutes"].insert_all(pdf_list, pk="url")
db["minutes"].enable_fts(["text"])