# Extract text from pdf (pdf scanned as images)

# pdf2image.convert_from_path()	PDF (scanned pages) → Images (JPG/PNG in memory)
# pytesseract.image_to_string()	Images → Extracted Arabic text (string)
import os
import re
import pytesseract
from pdf2image import convert_from_path
from dotenv import load_dotenv

# Load the .env file from the project root
load_dotenv()

def Extract_text(pdf_path, dpi=200, lang='ara'):
    # ---------- Read ALL paths from .env ----------
    tesseract_cmd = os.getenv('TESSERACT_CMD')
    poppler_path = os.getenv('POPPLER_PATH')
    tessdata_prefix = os.getenv('TESSDATA_PREFIX')



    # ---------- If any path is missing, stop and tell the user ----------
    if not tesseract_cmd:
        raise ValueError("TESSERACT_CMD not found in .env file!")
    if not poppler_path:
        raise ValueError("POPPLER_PATH not found in .env file!")
    if not tessdata_prefix:
        raise ValueError("TESSDATA_PREFIX not found in .env file!")



    # ---------- Tell Tesseract where the .exe is ----------
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    # ---------- Tell Tesseract where the Arabic language file is ----------
    os.environ['TESSDATA_PREFIX'] = tessdata_prefix

    # ---------- Check if the PDF exists ----------
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")



    # ---------- Convert PDF to images ----------
    print("Converting PDF to images...")
    images = convert_from_path(pdf_path, dpi=dpi, poppler_path=poppler_path)
    print(f"Converted {len(images)} pages.")


    # ---------- OCR each page ----------
    all_text = ""
    for page_num, image in enumerate(images, start=1):
        text = pytesseract.image_to_string(image, lang=lang)
        if text and text.strip():
            all_text += text + " "
            if page_num % 10 == 0:
                print(f"Page {page_num}/{len(images)} processed.")


    # ---------- Clean the text ----------
    cleaned_text = re.sub(r'\s+', ' ', all_text).strip()
    print(f"Total extracted characters: {len(cleaned_text):,}")
    return cleaned_text




# -------------------------------------------------------------------




# save txt file 
def clean_and_save(data, book_title):
    """
    Cleans the raw OCR text, splits it into paragraphs (using PARAGRAPH_SIZE from .env),
    and saves it to a .txt file in the 'Data as text' folder.
    """

    # ----------  Clean the text ----------
    cleaned = re.sub(r'[\u200B-\u200F\u061C\uFEFF]', '', data)          # Remove invisible Arabic marks
    cleaned = re.sub(r'\s+', ' ', cleaned)                              # Normalize spaces
    cleaned = re.sub(r'\s*\.\s*\.\s*', '. ', cleaned)                   # Fix " . . " → ". "
    cleaned = re.sub(r'\.+', '.', cleaned)                              # Fix "...." → "."
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()                      # Final space cleanup


    # ----------  Split into sentences ----------
    sentences = re.split(r'(?<=[.!?])\s+', cleaned)

    # ---------- Read PARAGRAPH_SIZE from .env ----------
    PARAGRAPH_SIZE = int(os.getenv('PARAGRAPH_SIZE', 5))


    # ---------- Group sentences into paragraphs ----------
    paragraphs = []
    for i in range(0, len(sentences), PARAGRAPH_SIZE):
        group = ' '.join(sentences[i:i+PARAGRAPH_SIZE])
        if group.strip():
            paragraphs.append(group.strip())


    # Join paragraphs with double newlines
    final_text = '\n'.join(paragraphs)

    # ---------- Create the folder (if it doesn't exist) ----------
    os.makedirs("Data as text", exist_ok=True)


    # ---------- Add .txt extension if missing ----------
    if not book_title.endswith(".txt"):
        book_title += ".txt"


    # ---------- Build the full path and save ----------
    output_path = os.path.join("Data as text", book_title)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_text) 

    print('Done')
    print(f'type ---> {type(final_text)}')
    return final_text





    