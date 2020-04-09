from .bitmap import Bitmap

class Page:
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
        self.FPDF_ClosePage(self.handle)
        self.handle = None
        self.lib = None
        self.dll = None
        self.check = None

    def width(self):
        return self.FPDF_GetPageWidthF(self.handle)

    def height(self):
        return self.FPDF_GetPageHeightF(self.handle)

    def thumbnail(self, *, nbytes=False, raw=False, bitmap=False):
        assert (raw or bitmap) and not (raw and bitmap)
        if raw:
            nb = self.FPDFPage_GetRawThumbnailData(self.handle, self.lib.ffi.NULL, 0)
            if nbytes:
                return nb
            if nb == 0:
                return 0, None
            b = bytes(b'\0' * nb)
            nb = self.FPDFPage_GetRawThumbnailData(self.handle, b, nb)
            return nb, b
        if bitmap:
            return self.FPDFPage_GetThumbnailAsBitmap(self.handle)
        nb = self.FPDFPage_GetDecodedThumbnailData(self.handle, self.lib.ffi.NULL, 0)
        if nbytes:
            return nb
        if nb == 0:
            return 0, None
        b = bytes(b'\0' * nb)
        nb = self.FPDFPage_GetDecodedThumbnailData(self.handle, b, nb)
        return nb, b

    def render(self, x, y, width, height, rotate, flags):
        bitmap = self.FPDFBitmap_Create(width, height, 0)
        self.FPDF_RenderPageBitmap(bitmap, self.handle, x, y, width, height, rotate, flags)
        return Bitmap(self.lib, bitmap)
