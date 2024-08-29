# Required modules can be installed using:
# pip install -r requirements.txt

import os
from PIL import Image
import pytesseract
from tqdm import tqdm
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# Set the path to the Tesseract executable
# Uncomment and modify the following line if Tesseract is not in your system PATH
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def process_image(image_path):
    """
    Process a single image and return the extracted text.
    """
    try:
        with Image.open(image_path) as img:
            text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")
        return ""


def process_directory(input_dirs, output_file):
    """
    Process all images in the input directories and save results to a single flowing PDF file.
    """
    all_texts = []

    for input_dir in input_dirs:
        image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(
            ('.png', '.jpg', '.jpeg', '.tiff', '.bmp'))]

        # Sort files by creation time
        image_files.sort(key=lambda x: os.path.getctime(
            os.path.join(input_dir, x)))

        for image_file in tqdm(image_files, desc=f"Processing images in {input_dir}"):
            input_path = os.path.join(input_dir, image_file)
            text = process_image(input_path)
            all_texts.append(text)

    # Create PDF
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    for text in all_texts:
        story.append(Paragraph(text, styles['BodyText']))

    doc.build(story)


if __name__ == "__main__":
    # Get the current working directory (root of the project)
    root_dir = os.getcwd()

    input_directories = [
        os.path.join(root_dir, "images")
    ]
    output_file = os.path.join(root_dir, "ocr_output.pdf")

    process_directory(input_directories, output_file)
    print("OCR processing complete! PDF created.")
