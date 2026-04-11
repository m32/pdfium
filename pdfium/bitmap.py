from PIL import Image

class Bitmap:
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
        self.FPDFBitmap_Destroy(self.handle)
        self.handle = None
        self.lib = None
        self.dll = None
        self.check = None

    def format(self):
        return self.FPDFBitmap_GetFormat(self.handle)

    def width(self):
        return self.FPDFBitmap_GetWidth(self.handle)

    def height(self):
        return self.FPDFBitmap_GetHeight(self.handle)

    #extern void  FPDFBitmap_FillRect(FPDF_BITMAP bitmap, int left, int top, int width, int height, FPDF_DWORD color);

    def image(self):
        b = self.FPDFBitmap_GetBuffer(self.handle)
        w = self.width()
        h = self.height()
        buffer = self.lib.ffi.buffer(b, w * h * 3) # RGB
        b = bytes(buffer)

        img = Image.frombuffer("RGB", (w, h), b, "raw", "BGR", w*3, 1)
        return img
