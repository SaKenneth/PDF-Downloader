import pandas as pd
import PyPDF2
from pathlib import Path
import shutil, os
import os.path
import urllib.request, urllib.error, urllib.parse
import glob
import socket
import concurrent.futures
from more_itertools import grouper


socket.setdefaulttimeout(30)

class pdfDownloader:
    def __init__(self, list_pth, pth, ID):
        self.list_pth = list_pth
        self.pth = pth
        self.ID = ID
        self.dwn_pth = pth + "dwn/"
        self.dwn_files = glob.glob(os.path.join(self.dwn_pth, "*.pdf")) 
        self.exist = [os.path.basename(f)[:-4] for f in self.dwn_files]
        self.df = pd.read_excel(list_pth, sheet_name=0, index_col=ID)
        self.non_empty = self.df.Pdf_URL.notnull() == True
        self.df = self.df[self.non_empty]
        self.df2 = self.df.copy()

    def download(self, j):
            if j not in self.exist:
                savefile = str(self.pth + "dwn/" + str(j) + '.pdf')
                try:
                    urllib.request.urlretrieve(self.df2.at[j,'Pdf_URL'], savefile)
                    try:
                        self.check(j, savefile)
                    except Exception as e:
                        self.df2.at[j,"error"] = str(e)
                        # print("Error opening file", j, str(e))
                except Exception as e:
                    self.df2.at[j,"error"] = str(e)
                    # print("Error downloading file", j, str(e))

                    try:
                        urllib.request.urlretrieve(self.df2.at[j,'Report Html Address'], savefile)
                        try:
                            self.check(j, savefile)
                        except Exception as e:
                            self.df2.at[j,"error"] = str(e)
                            # print("Error opening file", j, str(e))
                    except Exception as e:
                        self.df2.at[j,"error"] = str(e)
                        # print("Error downloading file", j, str(e))


    # check if pdf if empty or can be opened
    def check(self, j, savefile):
        try:
            pdfFileObj = open(savefile, 'rb')
            pdfReader = PyPDF2.PdfReader(pdfFileObj)
            if pdfReader.is_encrypted:
                pdfReader.decrypt('')
            if len(pdfReader.pages) == 0:
                self.df2.at[j,"error"] = "Empty"
                print("Empty file", j)
                pdfFileObj.close()
                os.remove(savefile)
            else:
                self.df2.at[j,"error"] = "OK"
                print("OK file", j)
        except Exception as e:
            self.df2.at[j,"error"] = str(e)
            # print("Error opening file", j, str(e))
            pdfFileObj.close()
            os.remove(savefile)

    def save(self):
        self.df2.to_excel(self.pth + "pdf_downloads.xlsx")

    def threader(self, func, args, n=500):
        with concurrent.futures.ThreadPoolExecutor(max_workers=n) as executor:
            executor.map(func, args)

    def run(self):
        self.threader(self.download, self.df2.index)
        self.save()

if __name__ == "__main__":
    pth = ""
    list_pth = pth + "GRI_2017_2020.xlsx"
    ID = "BRnum"
    pdf = pdfDownloader(list_pth, pth, ID)
    pdf.run()