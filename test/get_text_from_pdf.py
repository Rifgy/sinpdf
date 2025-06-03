import pdfplumber.display

def get_text_from_pdf(path:str):
    text = (pdfplumber.display.pypdfium2.PdfDocument(path).
            get_page(0).
            get_textpage().
            get_text_range())
    print(text)

if __name__ == "__main__":
    #file = "/home/usver/CODI/_TEST_DATA_/test.pdf"
    file = "/home/usver/CODI/_TEST_DATA_/test_data/ХФ ПМ УК 2023/ПМУК-2_02-001_от_10.01.2023_О_реализации_производственно-инвестицио_проектов_в_2023_год_(11672577_v1).PDF"
    get_text_from_pdf(file)
    pass