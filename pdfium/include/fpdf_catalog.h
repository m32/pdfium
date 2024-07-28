// Copyright 2017 The PDFium Authors
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// Experimental API.
//
// Determine if |document| represents a tagged PDF.
//
// For the definition of tagged PDF, See (see 10.7 "Tagged PDF" in PDF
// Reference 1.7).
//
//   document - handle to a document.
//
// Returns |true| iff |document| is a tagged PDF.
extern FPDF_BOOL 
FPDFCatalog_IsTagged(FPDF_DOCUMENT document);
