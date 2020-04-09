#!/usr/bin/env vpython3
import time
from pdfium.pdfium import PDFium

class Demo:
    def __init__(self, lib):
        self.lib = lib

    def Demo(self):
        fname = 'Acrobat_DigitalSignatures_in_PDF.pdf'
        password = self.lib.ffi.NULL
        print('File:', fname)
        try:
            doc = self.lib.document(fname.encode(), password)
        except IOError as ex:
            print('Error:', ex.errno, ex.args)
            return
        try:
            pc = doc.PageCount()
            print('Pages:', pc)
            title = doc.Title()
            print('Title:', title)
            for pageno in range(pc):
                page = doc.Page(pageno)
                print('page:', pageno, 'size:', page.width(), page.height())
                try:
                    data = page.thumbnail(nbytes=False, raw=True, bitmap=False)
                    if data[1] is None:
                        print('no thumbnail')
                    n = 5
                    bmp = page.render(0, 0, 600*n, 800*n, 0, 0)
                    try:
                        img = bmp.image()
                        #img.save('page0.jpg', 'JPEG', quality=80)
                        img.save('page%02d.png'%pageno, 'PNG')
                    finally:
                        bmp.close()
                finally:
                    page.close()
        finally:
            doc.close()

def main():
    dll = PDFium()
    cls = Demo(dll)
    try:
        cls.Demo()
    finally:
        dll.close()

main()


