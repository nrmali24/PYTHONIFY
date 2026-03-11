import os
from loguru import logger
from .tika_client import extract_text
from .converter import convert_to_pdf

MAX_FILE_SIZE = 200 * 1024 * 1024


class Extractor:

    def validate(self, file_path):

        if not os.path.exists(file_path):
            raise Exception("file not found")

        size = os.path.getsize(file_path)

        if size > MAX_FILE_SIZE:
            raise Exception("file too large")

    def extract(self, file_path):

        self.validate(file_path)

        try:

            logger.info("trying tika primary")

            text = extract_text(file_path)

            if text.strip():
                return text

        except Exception as e:

            logger.warning(f"tika failed {e}")

        try:

            logger.info("fallback libreoffice")

            pdf = convert_to_pdf(file_path)

            text = extract_text(pdf)

            return text

        except Exception as e:

            logger.error(f"fallback failed {e}")

        raise Exception("extraction failed")