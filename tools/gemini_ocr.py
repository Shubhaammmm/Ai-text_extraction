import os
import tempfile
import requests
from pdf2image import convert_from_path
import google.generativeai as genai

# Configure Gemini API
os.environ['GEMINI_AI_API_KEY'] = ""
API_KEY = os.environ['GEMINI_AI_API_KEY']
genai.configure(api_key=API_KEY)


def download_pdf(url):
    """Download a PDF from a URL to a temporary file."""
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        with open(temp_pdf.name, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Downloaded PDF to: {temp_pdf.name}")
        return temp_pdf.name
    else:
        raise Exception(f"Failed to download PDF: {response.status_code}")


def convert_pdf_to_images(pdf_path, output_folder):
    images = convert_from_path(pdf_path, dpi=300)
    image_paths = []
    for i, image in enumerate(images):
        image_file = os.path.join(output_folder, f"page_{i+1}.png")
        image.save(image_file, "PNG")
        image_paths.append(image_file)
    return image_paths


def prep_image(image_path):
    sample_file = genai.upload_file(path=image_path, display_name="Page Image")
    file = genai.get_file(name=sample_file.name)
    return sample_file


def extract_text_from_image(image, prompt):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash-8b")
    response = model.generate_content([image, prompt])
    return response.text.replace("\n", " ").strip()


def process_pdf(pdf_path, prompt):
    extracted_texts = []
    try:
        with tempfile.TemporaryDirectory() as temp_folder:
            image_files = convert_pdf_to_images(pdf_path, temp_folder)
            for image_file in image_files:
                sample_file = prep_image(image_file)
                text = extract_text_from_image(sample_file, prompt)
                if text:
                    extracted_texts.append(text)
    except Exception as e:
        print(f"Error in process_pdf: {str(e)}")
    return extracted_texts


def run(message: str, params: dict):
    try:
        url = params.get("url")

        if not url:
            return {"status": "error", "message": "The 'url' parameter is required."}

        if not message or message.strip() == "":
            return {"status": "error", "message": "The 'message' prompt is required."}

        # Handle remote URLs or local file paths
        if url.startswith("http://") or url.startswith("https://"):
            pdf_path = download_pdf(url)
        elif os.path.exists(url):
            pdf_path = url
        else:
            return {"status": "error", "message": f"Invalid file path or URL: {url}"}

        extracted_texts = process_pdf(pdf_path, message)

        if not extracted_texts:
            return {"status": "error", "message": "No text was extracted from the PDF."}

        return {"status": "success", "data": {"extracted_texts": extracted_texts}}

    except Exception as e:
        return {"status": "error", "message": str(e)}
