// Copyright 2014 The PDFium Authors
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// Original code copyright 2014 Foxit Software Inc. http://www.foxitsoftware.com

// Flatten operation failed.
#define FLATTEN_FAIL 0
// Flatten operation succeed.
#define FLATTEN_SUCCESS 1
// Nothing to be flattened.
#define FLATTEN_NOTHINGTODO 2

// Flatten for normal display.
#define FLAT_NORMALDISPLAY 0
// Flatten for print.
#define FLAT_PRINT 1

// Flatten annotations and form fields into the page contents.
//
//   page  - handle to the page.
//   nFlag - One of the |FLAT_*| values denoting the page usage.
//
// Returns one of the |FLATTEN_*| values.
//
// Currently, all failures return |FLATTEN_FAIL| with no indication of the
// cause.
extern int  FPDFPage_Flatten(FPDF_PAGE page, int nFlag);
