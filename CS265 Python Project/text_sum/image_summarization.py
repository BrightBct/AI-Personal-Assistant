import io
import pytesseract
import requests

from PIL import Image
from summarization.sum_function import search as search_summary
from summarization.sum_function import text_summarization


def image_sum(model, tokenizer, device):
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    url = input("Image Link Url: ")
    res = requests.get(url)
    img = Image.open(io.BytesIO(res.content))
    text = pytesseract.image_to_string(img)
    summary = search_summary(text, False)
    summary = text_summarization(summary, model, tokenizer, device)
    print("Summary: "+summary)
    print()
