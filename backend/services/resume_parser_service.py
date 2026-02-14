import io
import re
from dataclasses import dataclass


@dataclass
class ParsedResume:
    text: str
    file_type: str


class ResumeParserService:
    def parse(self, file_bytes: bytes, filename: str) -> ParsedResume:
        if not filename:
            raise ValueError("Resume file name is required")

        suffix = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""
        if suffix == "txt":
            text = file_bytes.decode("utf-8", errors="ignore")
        elif suffix == "pdf":
            text = self._parse_pdf(file_bytes)
        elif suffix == "docx":
            text = self._parse_docx(file_bytes)
        else:
            raise ValueError("Unsupported resume format. Use .txt, .pdf, or .docx")

        cleaned = self._clean_text(text)
        if not cleaned:
            raise ValueError("Could not extract readable text from resume")

        return ParsedResume(text=cleaned, file_type=suffix)

    @staticmethod
    def _parse_pdf(file_bytes: bytes) -> str:
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise RuntimeError("pypdf is required for PDF parsing") from exc

        reader = PdfReader(io.BytesIO(file_bytes))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages)

    @staticmethod
    def _parse_docx(file_bytes: bytes) -> str:
        try:
            from docx import Document
        except ImportError as exc:
            raise RuntimeError("python-docx is required for DOCX parsing") from exc

        doc = Document(io.BytesIO(file_bytes))
        return "\n".join(paragraph.text for paragraph in doc.paragraphs)

    @staticmethod
    def _clean_text(value: str) -> str:
        value = value.replace("\x00", " ")
        value = re.sub(r"\s+", " ", value).strip()
        return value
