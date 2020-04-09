from .page import Page

class Document:
    def __init__(self, lib, handle):
        self.lib = lib
        self.handle = handle
        self.check = lib.check
        self.dll = lib.dll

    def __getattr__(self, name):
        proc = getattr(self.dll, name)
        class Wrap:
            def __call__(this, *args, **kwargs):
                result = proc(*args, **kwargs)
                self.lib.check(name)
                return result
        return Wrap()

    def close(self):
        self.FPDF_CloseDocument(self.handle)
        self.handle = None
        self.lib = None
        self.dll = None
        self.check = None

    def PageCount(self):
        return self.FPDF_GetPageCount(self.handle)

    def Title(self, bookmark=None):
        if bookmark is None:
            bookmark = self.FPDFBookmark_GetFirstChild(self.handle, self.lib.ffi.NULL)
        nb = self.FPDFBookmark_GetTitle(bookmark, self.lib.ffi.NULL, 0)
        b = bytes(b'\0'*nb)
        nb = self.FPDFBookmark_GetTitle(bookmark, b, nb)
        self.check('FPDFBookmark_GetTitle')
        return b.decode('utf-16le')

    def Page(self, page):
        return Page(self.lib, self.FPDF_LoadPage(self.handle, page))
