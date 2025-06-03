from pathlib import Path

def get_files_from_path(pathtodir: str) -> int:

    if pathtodir:
        target_dir = Path(pathtodir)
        pdf_files = list(target_dir.rglob('*.pdf'))  # Получаем список всех PDF-файлов

        for index, entry in enumerate(pdf_files):
            print(f"{entry.name}\n\t\t{entry.as_posix()}")
            index += 1
        return len(pdf_files)
    else:
        print('Select folder error', 'Please select directory with files')
        return 0

if __name__ == "__main__":
    pass
    #pth = "Y:\\146 Канцелярия\\Общая\\Приказы"
    #pth = "Y:\\146 Канцелярия\\Общая\\Распоряжения"
    #pth = "Y:\\146 Канцелярия\\Общая"
    #pth = "/home/usver"
    #print(f"File count: {get_files_from_path(pth)}")

'''
C:\Users\nikolchuk\PycharmProjects\sinpdf\.venv\Scripts\python.exe "C:/Program Files/JetBrains/PyCharm Community Edition 2025.1.1.1/plugins/python-ce/helpers/pydev/pydevconsole.py" --mode=client --host=127.0.0.1 --port=56279 
import sys; print('Python %s on %s' % (sys.version, sys.platform))
sys.path.extend(['C:\\Users\\nikolchuk\\PycharmProjects\\sinpdf', 'C:\\Users\\nikolchuk\\PycharmProjects\\sinpdf\\sinpdf'])
PyDev console: starting.
Python 3.13.3 (tags/v3.13.3:6280bb5, Apr  8 2025, 14:47:33) [MSC v.1943 64 bit (AMD64)] on win32
runfile('C:\\Users\\nikolchuk\\PycharmProjects\\sinpdf\\sinpdf\\main.py', wdir='C:\\Users\\nikolchuk\\PycharmProjects\\sinpdf\\sinpdf')
Traceback (most recent call last):
  File "C:\Users\nikolchuk\PycharmProjects\sinpdf\.venv\Lib\site-packages\pdfplumber\pdf.py", line 50, in __init__
    self.doc = PDFDocument(PDFParser(stream), password=password or "")
               ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\nikolchuk\PycharmProjects\sinpdf\.venv\Lib\site-packages\pdfminer\pdfdocument.py", line 738, in __init__
    raise PDFSyntaxError("No /Root object! - Is this really a PDF?")
pdfminer.pdfparser.PDFSyntaxError: No /Root object! - Is this really a PDF?
During handling of the above exception, another exception occurred:
Traceback (most recent call last):
  File "C:\Users\nikolchuk\PycharmProjects\sinpdf\sinpdf\main.py", line 187, in get_files_from_path
    meta = get_pdf_meta(entry, GET_META_FROM_PDF)
  File "C:\Users\nikolchuk\PycharmProjects\sinpdf\sinpdf\functions.py", line 35, in get_pdf_meta
    with pdfplumber.open(path) as pdf:
         ~~~~~~~~~~~~~~~^^^^^^
  File "C:\Users\nikolchuk\PycharmProjects\sinpdf\.venv\Lib\site-packages\pdfplumber\pdf.py", line 107, in open
    return cls(
        stream,
    ...<7 lines>...
        raise_unicode_errors=raise_unicode_errors,
    )
  File "C:\Users\nikolchuk\PycharmProjects\sinpdf\.venv\Lib\site-packages\pdfplumber\pdf.py", line 52, in __init__
    raise PdfminerException(e)
pdfplumber.utils.exceptions.PdfminerException: No /Root object! - Is this really a PDF?
Process finished with exit code 0

'''