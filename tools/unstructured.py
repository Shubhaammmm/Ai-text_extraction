import os
import tempfile
import warnings
import requests
from unstructured.partition.pdf import partition_pdf
from unstructured.partition.doc import partition_doc
from unstructured.partition.docx import partition_docx
from unstructured.partition.csv import partition_csv
from unstructured.partition.xlsx import partition_xlsx
from unstructured.partition.text import partition_text
from unstructured.partition.pptx import partition_pptx
from unstructured.partition.odt import partition_odt
from unstructured.partition.tsv import partition_tsv
from unstructured.partition.ppt import partition_ppt
from unstructured.partition.ndjson import partition_ndjson

warnings.filterwarnings('ignore')


def download_file(url):
    """
    Download a file from a given URL.

    :param url: The URL of the file.
    :return: The local path of the downloaded file.
    """
    try:
        response = requests.get(url, stream=True,verify=False)
        if response.status_code == 200:
            suffix = os.path.splitext(url.split("?")[0])[1]  # Get file extension
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            with open(temp_file.name, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Downloaded file from {url} to {temp_file.name}")
            return temp_file.name
        else:
            raise Exception(f"Failed to download file: {response.status_code}")
    except Exception as e:
        raise Exception(f"Error downloading file: {str(e)}")


def extract_text(file_path):
    """
    Extracts text based on file type using unstructured library.
    """
    try:
        ext = os.path.splitext(file_path)[1].lower()

        if ext in [".pdf"]:
            elements = partition_pdf(filename=file_path)
        elif ext in [".doc"]:
            elements = partition_doc(filename=file_path)
        elif ext in [".docx"]:
            elements = partition_docx(filename=file_path)
        elif ext in [".csv"]:
            elements = partition_csv(filename=file_path)
        elif ext in [".xlsx"]:
            elements = partition_xlsx(filename=file_path)
        elif ext in [".txt"]:
            elements = partition_text(filename=file_path)
        elif ext in [".pptx"]: 
            elements = partition_pptx(filename=file_path)
        elif ext in [".ppt"]: 
            elements = partition_ppt(filename=file_path)
        elif ext in [".odt"]: 
            elements = partition_odt(filename=file_path)
        elif ext in [".tsv"]: 
            elements = partition_tsv(filename=file_path)
        elif ext in [".ndjson"]: 
            elements = partition_ndjson(filename=file_path)                
        else:
            return f"Unsupported file type: {ext}"

        extracted_text = "\n".join([el.text for el in elements if el.text])
        return extracted_text.strip()

    except Exception as e:
        return f"Error extracting text: {str(e)}"


def extract_scanned_pdf(file_path):
    """
    Extract text from a scanned PDF using OCR.
    """
    try:
        elements = partition_pdf(filename=file_path, strategy="hi_res", ocr_languages="eng")
        extracted_text = "\n".join([el.text for el in elements if el.text])
        return extracted_text.strip()
    except Exception as e:
        return f"Error extracting text using OCR: {str(e)}"


def run(message: str, params: dict):
    """
    Run function to execute the file-to-text pipeline.
    Decides dynamically whether to use normal or OCR extraction.
    """
    try:
        url = params.get("url")
        if not url:
            return {"status": "error", "message": "The 'url' parameter is required."}

        # Download or use local file
        if url.startswith("http://") or url.startswith("https://"):
            file_path = download_file(url)
        elif os.path.exists(url):
            file_path = url
        else:
            return {"status": "error", "message": f"Invalid file path or URL: {url}"}

        extracted_text = extract_text(file_path)

        # Handle scanned PDFs with OCR
        if file_path.endswith(".pdf") and (not extracted_text or len(extracted_text.split()) < 10):
            print("Attempting OCR extraction for possible scanned PDF...")
            extracted_text = extract_scanned_pdf(file_path)

        if not extracted_text:
            return {"status": "error", "message": "No text was extracted from the file."}

        return {"status": "success", "data": {"extracted_text": extracted_text}}

    except Exception as e:
        return {"status": "error", "message": str(e)}
     
