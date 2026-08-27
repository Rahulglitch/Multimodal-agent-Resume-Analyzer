# utils/doc_parser.py

from io import BytesIO

from docx import Document


def extract_docx_text(file_bytes):

    try:

        document = Document(
            BytesIO(file_bytes)
        )

        text_parts = []

        for paragraph in document.paragraphs:

            if paragraph.text.strip():

                text_parts.append(
                    paragraph.text
                )

        result = "\n".join(
            text_parts
        )

        if not result.strip():

            raise ValueError(
                "No readable text found in DOCX."
            )

        return result

    except Exception as error:

        raise ValueError(
            f"Unable to read DOCX file: {error}"
        )
