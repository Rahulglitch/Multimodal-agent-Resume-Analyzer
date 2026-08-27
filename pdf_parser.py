# utils/pdf_parser.py

import pymupdf


def extract_pdf_text(file_bytes):

    document = None

    try:

        document = pymupdf.open(
            stream=file_bytes,
            filetype="pdf"
        )

        if document.page_count == 0:

            raise ValueError(
                "PDF contains no pages."
            )

        text_parts = []

        for page in document:

            text_parts.append(
                page.get_text()
            )

        text = "\n".join(text_parts)

        if not text.strip():

            raise ValueError(
                "No readable text found in PDF."
            )

        return text

    finally:

        if document is not None:

            document.close()
