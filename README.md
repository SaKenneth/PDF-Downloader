
# PDF-Downloader

To download PDF Files from a given excel file with the provided ID as the name of the PDF files.


## Run Locally

Clone the project

```bash
  git clone https://github.com/SaKenneth/PDF-Downloader.git
```

Go to the project directory

```bash
  cd PDF-Downloader
```

Install dependencies

```bash
  pip install -r requirements.txt
```
at the buttom of the .py script you will see a **pth** and **list_pth**

- **pth** is the path to where you want the downloaded pdfs to end up.
- **list_path** as well as name for the excel file with the links to the PDFs By default the script will look for the given excel name in the same place as the script as well as place the PDFs in a dwn folder under the script. both values can be changed by adding the respective path in between the ``" "``

Start the script

```bash
  python pdfDownloader.py
```


## Features

- Able to download PDFs from excel files
- Checks if the PDF is accessible.
- Places the downloaded PDFs in the designated location

