#!/usr/bin/env vpython3
import sys
import time
from pdfium.pdfium import PDFium

class Demo:
    def __init__(self, lib):
        self.lib = lib

    def SavePage(self, doc, pageno, scale=6):
        page = doc.Page(pageno)
        width = int(page.width() * scale)
        height = int(page.height() * scale)
        print('page:', pageno, 'size:', width, height)
        try:
            data = page.thumbnail(nbytes=False, raw=True, bitmap=False)
            if data[1] is None:
                print('no thumbnail')
            bmp = page.render(0, 0, width, height, 0, 0)
            try:
                img = bmp.image()
                #img.save('page0.jpg', 'JPEG', quality=80)
                img.save('page%02d.png'%pageno, 'PNG')
            finally:
                bmp.close()
        finally:
            page.close()

    def SavePages(self, doc):
        pc = doc.PageCount()
        for pageno in range(pc):
            self.SavePage(doc, pageno)
            if pageno == 5:
                break

    def SigInfo(self, doc):
        nsig = doc.FPDF_GetSignatureCount(doc.handle)
        print('Numer of signatures:', nsig)
        for n in range(nsig):
            print('signature:', n)
            sig = doc.FPDF_GetSignatureObject(doc.handle, n)
            nb = doc.FPDFSignatureObj_GetContents(sig, doc.lib.ffi.NULL, 0)
            if nb:
                buf = bytes(b'\0'*nb)
                nb = doc.FPDFSignatureObj_GetContents(sig, buf, nb)
                #print(buf)
            nb = doc.FPDFSignatureObj_GetReason(sig, doc.lib.ffi.NULL, 0)
            if nb:
                buf = bytes(b'\0'*nb)
                nb = doc.FPDFSignatureObj_GetReason(sig, buf, nb)
                buf = buf.decode('utf-16le')
            else:
                buf = 'undefined'
            print('    reason:', buf)
            nb = doc.FPDFSignatureObj_GetTime(sig, doc.lib.ffi.NULL, 0)
            if nb:
                buf = bytes(b'\0'*nb)
                nb = doc.FPDFSignatureObj_GetTime(sig, buf, nb)
            else:
                buf = 'undefined'
            print('    time:', buf)
            mdp = doc.FPDFSignatureObj_GetDocMDPPermission(sig)
            print('    mdp:', mdp)

    def PageInfo(self, doc, pageno):
        page = doc.Page(pageno)
        try:
            width = page.width()
            height = page.height()
            print('page:', pageno, 'size:', width, height)
            nb = doc.FPDFPage_CountObjects(page.handle)
            for i in range(nb+1):
                obj = doc.FPDFPage_GetObject(page.handle, i)
                objtype = doc.FPDFPageObj_GetType(obj)
                if objtype == doc.dll.FPDF_PAGEOBJ_TEXT:
                    print(i, obj, 'text')
                else:
                    print(i, obj, objtype)
        finally:
            page.close()

    def Demo(self):
        fname = sys.argv[1]
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
            self.SigInfo(doc)
            self.PageInfo(doc, 1)
            self.SavePages(doc)
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
