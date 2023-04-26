from io import BytesIO
import requests
from bs4 import BeautifulSoup
from dateutil.parser import *
import pdfplumber
from playhouse.sqlite_ext import *
db = SqliteExtDatabase('ethics.db')

# Define the Minute model for storing meeting minutes
class Minute(Model):
    date = DateField()
    file = CharField()
    url = CharField()
    text = TextField()

    class Meta:
        table_name = "minutes"
        database = db

# Define the MinuteIndex model for full-text search
class MinuteIndex(FTSModel):
    rowid = RowIDField()
    text = SearchField()

    class Meta:
        database = db
        options = {'tokenize': 'porter', 'content': Minute.text}

# Create the database tables
db.create_tables([Minute, MinuteIndex])

# Set the base URL for meeting minutes
base_url = "https://ethics.maryland.gov/meeting-minutes/?wpfb_list_page="

# Loop through the pages containing the meeting minutes
for page in range(1,9):
    url = base_url + str(page)
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    # Find all the PDF links on the page
    pdf_links = [x for x in soup.find_all('p') if x.find('a')]

    # Process each PDF link
    for link in pdf_links:
        # Extract and parse the date from the link text
        date = parse(link.text.strip())
        
        # Extract the PDF URL and filename
        pdf_url = link.find('a')['href']
        name = pdf_url.split('/')[-1].replace('.pdf','')
        
        # Download and open the PDF
        pdf = requests.get(pdf_url)
        with pdfplumber.open(BytesIO(pdf.content)) as pdf:
            all_pages_text = ""
            
            # Extract text from each page in the PDF
            for page in pdf.pages:
                page_text = page.extract_text()
                all_pages_text += "\n" + page_text if page_text else ""
        
        # Save the meeting minute to the database
        Minute.create(date=date, file=name, url=pdf_url, text=all_pages_text)

# Rebuild and optimize the full-text search index
MinuteIndex.rebuild()
MinuteIndex.optimize()