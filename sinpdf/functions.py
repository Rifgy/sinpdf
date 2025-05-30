import os, sys, subprocess, datetime, socket

import pdfplumber

def get_local_hostname():
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

def parse_meta_datatime(dtsting:str):
    """
    Сonvertation of a string "D: 20120320133836+08'00 '" of metadata into the Datatime format

    :rtype: datetime
    :param dtsting
    :return: convert to datatime string or current datetime
    """
    if dtsting:
        dt = (dtsting.split(':')[1])[:14]
        return datetime.datetime.strptime(dt, '%Y%m%d%H%M%S')
    else:
        return datetime.datetime.now()

def get_pdf_meta(path, get_meta):
    """
    Return dict with PDF-metadata

    :param get_meta:
    :param path:
    :return:
    :rtype: dict[str, str | int] | str
    """
    with pdfplumber.open(path) as pdf:
        meta = dict(
            Creator='',
            Producer='',
            Author='',
            CreationDate='',
            ModDate='',
            PageCount=len(pdf.pages)
        )
        if get_meta:
            meta_pdf = pdf.metadata
            if meta_pdf:
                meta.update(meta_pdf)
                meta['CreationDate'] = parse_meta_datatime(meta['CreationDate'])
                meta['ModDate'] = parse_meta_datatime(meta['ModDate'])
                return meta
        else:
            return meta


def get_pdf_text(path:str, getpages:int):
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

                if page.page_number >getpages:
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
    pass