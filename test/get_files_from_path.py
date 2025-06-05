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
pdfminer.pdfparser.PDFSyntaxError: No /Root object! - Is this really a PDF?
  File "C:\Users\nikolchuk\PycharmProjects\sinpdf\sinpdf\main.py", line 187, in get_files_from_path
    meta = get_pdf_meta(entry, GET_META_FROM_PDF)
  File "C:\Users\nikolchuk\PycharmProjects\sinpdf\sinpdf\functions.py", line 35, in get_pdf_meta
    with pdfplumber.open(path) as pdf:
pdfplumber.utils.exceptions.PdfminerException: No /Root object! - Is this really a PDF?
Process finished with exit code 0
'''