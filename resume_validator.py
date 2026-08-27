# utils/resume_validator.py

from io import BytesIO

from pypdf import PdfReader
from docx import Document


MAX_FILE_SIZE = 10 * 1024 * 1024


def validate_resume(file):

    if file is None:

        return False, "No resume file was uploaded."


    # ========================================================
    # READ FILE
    # ========================================================

    try:

        file_bytes = file.getvalue()

    except Exception:

        return False, "Unable to read the uploaded file."


    # ========================================================
    # EMPTY
    # ========================================================

    if not file_bytes:

        return False, "The uploaded file is empty."


    # ========================================================
    # SIZE
    # ========================================================

    if len(file_bytes) > MAX_FILE_SIZE:

        return False, (
            "The uploaded file is too large. "
            "Maximum allowed size is 10 MB."
        )


    # ========================================================
    # EXTENSION
    # ========================================================

    filename = file.name.lower()


    if not filename.endswith(
        (".pdf", ".docx")
    ):

        return False, (
            "Unsupported file type. "
            "Please upload a PDF or DOCX resume."
        )


    # ========================================================
    # PDF
    # ========================================================

    if filename.endswith(".pdf"):

        if not file_bytes.startswith(b"%PDF"):

            return False, (
                "The uploaded file does not appear "
                "to be a valid PDF."
            )

        try:

            reader = PdfReader(
                BytesIO(file_bytes)
            )

            if reader.is_encrypted:

                return False, (
                    "Password-protected PDFs "
                    "are not supported."
                )

            if len(reader.pages) == 0:

                return False, (
                    "The PDF contains no pages."
                )

            text = ""

            for page in reader.pages:

                text += (
                    page.extract_text() or ""
                )

            if not text.strip():

                return False, (
                    "The PDF contains no readable text. "
                    "It may be a scanned resume."
                )

        except Exception as error:

            return False, (
                f"Unable to read PDF: {error}"
            )


    # ========================================================
    # DOCX
    # ========================================================

    elif filename.endswith(".docx"):

        if not file_bytes.startswith(b"PK"):

            return False, (
                "The uploaded file does not appear "
                "to be a valid DOCX file."
            )

        try:

            document = Document(
                BytesIO(file_bytes)
            )

            text = "\n".join(
                paragraph.text
                for paragraph in document.paragraphs
            )

            if not text.strip():

                return False, (
                    "The DOCX contains no readable text."
                )

        except Exception as error:

            return False, (
                f"Unable to read DOCX: {error}"
            )


    return True, "Resume file is valid."
