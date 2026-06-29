
from pypdf import PdfReader
from pathlib import Path
from pypdf import PdfReader


# ----------------reading the pdf------------
def read_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
       page_text = page.extract_text()
       if page_text:
         text += page_text+ "\n"  # Add a newline after each page's text

    return text

# ---------extracting text from resume pdf--------

def extract_text_from_pdf(uploaded_file):
    if uploaded_file is None:
       return ""
    
  
    
    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        text+= page.extract_text() or ""
        
    return text




# -------------reading the text file----------

def read_text_file(file_path: str) -> str:
    return Path(file_path).read_text(encoding="utf-8")


# -----------saving the uploaded file-------------
def save_uploaded_file(file_path:str, content:str) :
   
   file_path = Path(file_path)
   file_path.parent.mkdir(parents=True, exist_ok=True)
   file_path.write_text(content, encoding="utf-8")
   return file_path


