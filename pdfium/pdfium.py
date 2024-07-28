import os
import cffi

from .document import Document

# fpdf_formfill.h
def IS_XFA_FORMFIELD(t, lib):
    return t in (
        lib.ffi.FPDF_FORMFIELD_XFA,
        lib.ffi.FPDF_FORMFIELD_XFA_CHECKBOX,
        lib.ffi.FPDF_FORMFIELD_XFA_COMBOBOX,
        lib.ffi.FPDF_FORMFIELD_XFA_IMAGEFIELD,
        lib.ffi.FPDF_FORMFIELD_XFA_LISTBOX,
        lib.ffi.FPDF_FORMFIELD_XFA_PUSHBUTTON,
        lib.ffi.FPDF_FORMFIELD_XFA_SIGNATURE,
        lib.ffi.FPDF_FORMFIELD_XFA_TEXTFIELD,
    )

# fpdf_edit.h
def FPDF_ARGB(a, r, g, b):
    return (b&0xff) | ((g&0xff)<<8) | ((r&0xff)<<16) | ((a&0xff)<<26)
def FPDF_GetBValue(argb):
    return argb&0xff
def FPDF_GetGValue(argb):
    return (argb>>8)&0xff
def FPDF_GetRValue(argb):
    return (argb>>16)&0xff
def FPDF_GetAValue(argb):
    return (argb>>24)&0xff

class PDFiumError(Exception):
    def __init__(self, no, msg):
        self.no = no
        self.msg = msg
    def __str__(self):
        return 'PDFiumError: rc={} msg={}'.format(self.no, self.msg)
    __repr__ = __str__

class PDFium:
    def __init__(self):
        self.dname = '/'.join(__file__.split('/')[:-1])
        self.ffi = cffi.FFI()
        self.installffi()
        dllname = os.path.join(self.dname, 'libpdfiumjs.so')
        self.dll = self.ffi.dlopen(dllname)

        init_config = self.ffi.new("FPDF_LIBRARY_CONFIG *", (2,))
        self.dll.FPDF_InitLibraryWithConfig(init_config)
        self.check("FPDF_InitLibraryWithConfig")

    def close(self):
        self.dll.FPDF_DestroyLibrary()
        #self.check("FPDF_DestroyLibrary")

    def check(self, msg):
        rc = self.dll.FPDF_GetLastError()
        if rc != 0:
            raise PDFiumError(rc, msg)

    def document(self, fname, password):
        doc = self.dll.FPDF_LoadDocument(fname, password)
        self.check("FPDF_LoadDocument")
        return Document(self, doc)

    def installffi(self):
        for fname in (
            'fpdfview.h',
            'fpdf_doc.h',
            'fpdf_formfill.h',
            'fpdf_annot.h',
            'fpdf_attachment.h',
            'fpdf_catalog.h',
            'fpdf_dataavail.h',
            'fpdf_edit.h',
            'fpdf_ext.h',
            'fpdf_flatten.h',
            'fpdf_fwlevent.h',
            'fpdf_javascript.h',
            'fpdf_ppo.h',
            'fpdf_progressive.h',
            'fpdf_save.h',
            'fpdf_searchex.h',
            'fpdf_signature.h',
            'fpdf_structtree.h',
            'fpdf_sysfontinfo.h',
            'fpdf_text.h',
            'fpdf_thumbnail.h',
            'fpdf_transformpage.h',
        ):
            data = open(os.path.join(self.dname, 'include', fname), 'rt').read()
            self.ffi.cdef(data, packed=True)
