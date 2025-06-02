import os, sys, subprocess, socket
import pdfplumber

from pathlib import Path

def get_local_hostname() -> str:
    """
    Get local host name

    :rtype: str
    :param: none
    :return: host name
    """
    try:
        # get host domain name
        hostname = socket.gethostname()
        return hostname
    except Exception as e:
        if __name__ == "__main__":
            return f"Error when receiving the name of the host: {e}"
        else:
            return f'error: {e}'

def get_pdf_meta(path: Path, get_meta: bool) -> dict[str, str | int] | str:
    """
    Return dict with PDF-metadata

    :param path:
    :param get_meta:
    :return:
    :rtype: dict[str, str | int] | str
    """

    meta = dict(Creator='', Producer='', Author='', CreationDate='', ModDate='', PageCount=0)

    with pdfplumber.open(path) as pdf:
        print(f"path:{path}")
        meta['PageCount'] = len(pdf.pages)

        if get_meta:
            meta_pdf = pdf.metadata
            if meta_pdf:
                meta.update(meta_pdf)
    return meta


def get_pdf_text(path: Path, getpages: int):
    """
    Return PDF content in text mode format's

    :param path: Path to PDF file
    :param getpages: The number of pages in the PDF file to save
    :return: Content PDF-file in TEXT format

    """
    try:
        with pdfplumber.open(path) as pdf:
            text = ''
            for page in pdf.pages:
                # text extract
                text += page.extract_text(layout=True)

                # debug: болле быстрый, но более тупой
                #text += page.extract_text_simple()
                #debug: close curent page
                #page.close()

                if page.page_number > getpages:
                    break
        return text
    except Exception as e:
        if __name__ == "__main__":
            return f"Error when receiving the metadata of the PDF-file: {e}"
        else:
            return f'Failed to get text...'


def open_file_with_default(file_path):
    """

    :rtype: None
    :param file_path:
    """
    if sys.platform.startswith('win'):
        os.startfile(file_path)
    elif sys.platform == 'darwin':
        subprocess.call(['open', file_path])
    else:  # For Linux and others
        subprocess.call(['xdg-open', file_path])


if __name__ == "__main__":
    ph = "/home/usver/CODI/_TEST_DATA_/test_data/ХФ ПМ УК 2023/ПМУК-2_02-019_от_10.03.2023_Об_организации_полевых_работ_2023 испр.pdf"
    get_pdf_meta(ph, True)
    pass
