// Copyright 2014 The PDFium Authors
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// Original code copyright 2014 Foxit Software Inc. http://www.foxitsoftware.com

// Get the character index in |text_page| internal character list.
//
//   text_page  - a text page information structure.
//   nTextIndex - index of the text returned from FPDFText_GetText().
//
// Returns the index of the character in internal character list. -1 for error.
extern int 
FPDFText_GetCharIndexFromTextIndex(FPDF_TEXTPAGE text_page, int nTextIndex);

// Get the text index in |text_page| internal character list.
//
//   text_page  - a text page information structure.
//   nCharIndex - index of the character in internal character list.
//
// Returns the index of the text returned from FPDFText_GetText(). -1 for error.
extern int 
FPDFText_GetTextIndexFromCharIndex(FPDF_TEXTPAGE text_page, int nCharIndex);
