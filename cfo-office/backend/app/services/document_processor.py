import io
import os
import pdfplumber
import pandas as pd


def extract_text(filename: str, file_bytes: bytes) -> str:
    """Extract plain text from PDF, CSV, XLSX, or plain text files."""
    ext = os.path.splitext(filename)[1].lower()

    if ext == ".pdf":
        return _extract_pdf(file_bytes)
    elif ext == ".csv":
        return _extract_csv(file_bytes)
    elif ext in (".xlsx", ".xls"):
        return _extract_excel(file_bytes)
    elif ext in (".txt", ".md"):
        return file_bytes.decode("utf-8", errors="replace")
    else:
        # Best-effort UTF-8 decode
        return file_bytes.decode("utf-8", errors="replace")


def _extract_pdf(data: bytes) -> str:
    text_parts = []
    with pdfplumber.open(io.BytesIO(data)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
            # Also extract tables as markdown
            for table in page.extract_tables():
                if table:
                    rows = [" | ".join(str(c) if c else "" for c in row) for row in table]
                    text_parts.append("\n".join(rows))
    return "\n\n".join(text_parts)


def _extract_csv(data: bytes) -> str:
    df = pd.read_csv(io.BytesIO(data))
    return df.to_string(index=False)


def _extract_excel(data: bytes) -> str:
    xl = pd.ExcelFile(io.BytesIO(data))
    parts = []
    for sheet in xl.sheet_names:
        df = xl.parse(sheet)
        parts.append(f"### Sheet: {sheet}\n{df.to_string(index=False)}")
    return "\n\n".join(parts)
