# Full Text Search App
Example app for using full text search with SQLite

This example application uses [meeting minutes](https://ethics.maryland.gov/meeting-minutes/) from the Maryland State Ethics Commission, currently stored in PDF files. It scrapes those files, extracts the text from them using [pdfplumber](https://github.com/jsvine/pdfplumber) and inserts the data into a SQLite database, enabling full-text search on the column with the text.

To get started, run `bash setup.sh`