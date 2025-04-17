import os
import tempfile
import requests
import warnings
from unstructured.partition.pdf import partition_pdf

warnings.filterwarnings('ignore')

def download_pdf(url):
    """
    Download a PDF from a given URL and save it to a temporary file.

    :param url: The URL of the PDF file.
    :return: The local path of the downloaded file.
    """
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            with open(temp_pdf.name, "wb") as pdf_file:
                for chunk in response.iter_content(1024):
                    pdf_file.write(chunk)
            print(f"Downloaded PDF from {url} to {temp_pdf.name}")
            return temp_pdf.name  # Return the local file path
        else:
            raise Exception(f"Failed to download PDF: {response.status_code}")
    except Exception as e:
        raise Exception(f"Error downloading PDF: {str(e)}")

def extract(pdf_path):
    """
    Extracts text from a PDF file using unstructured.partition.pdf.

    :param pdf_path: Local path to the PDF file.
    :return: Extracted text from the PDF.
    """
    try:
        elements = partition_pdf(filename=pdf_path)
        extracted_text = "\n".join([cat.text for cat in elements if cat.text])
        return extracted_text.strip()
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def run(message: str, params: dict):
    """
    Run function to execute the PDF-to-text pipeline.

    :param message: The prompt message for text extraction.
    :param params: A dictionary containing parameters, including 'url' of the PDF.
    :return: A dictionary with the result of the operation.
    """
    try:
        # Extract the 'url' parameter
        url = params.get("url")
        if not url:
            return {"status": "error", "message": "The 'url' parameter is required."}
        # Determine if input is a local file or a URL
        if url.startswith("http://") or url.startswith("https://"):
            pdf_path = download_pdf(url)  # Download the PDF first
        elif os.path.exists(url):  
            pdf_path = url  # Local file
        else:
            return {"status": "error", "message": f"Invalid file path or URL: {url}"}

        # Call extract function
        extracted_text = extract(pdf_path)

        if not extracted_text:
            return {"status": "error", "message": "No text was extracted from the PDF."}

        return {"status": "success", "data": {"extracted_text": extracted_text}}

    except Exception as e:
        return {"status": "error", "message": str(e)}

