# Full Text Search App
Example app for using full text search with SQLite

This example application uses [meeting minutes](https://ethics.maryland.gov/meeting-minutes/) from the Maryland State Ethics Commission, currently stored in PDF files. It scrapes those files, extracts the text from them using [pdfplumber](https://github.com/jsvine/pdfplumber) and inserts the data into a SQLite database, enabling full-text search on the column with the text.

To get started, do the following in Terminal:

1. Run this command: `wget https://raw.githubusercontent.com/NewsAppsUMD/full_text_search_app/dev/setup.sh`
2. Run `bash setup.sh`
3. Run `mkdir .devcontainer`
4. Run `cd .devcontainer`
5. Run `wget https://raw.githubusercontent.com/NewsAppsUMD/full_text_search_app/dev/.devcontainer/Dockerfile`
6. Run `wget https://raw.githubusercontent.com/NewsAppsUMD/full_text_search_app/dev/.devcontainer/devcontainer.json`
7. Run `cd ..`
8. Rebuild the container when prompted.