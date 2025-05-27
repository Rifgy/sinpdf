import socket
import datetime
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
        dt = (dtsting.split(':')[1]).split('+')[0]
        return datetime.datetime.strptime(dt, '%Y%m%d%H%M%S')
    else:
        return datetime.datetime.now()

def get_pdf_meta(path:str):
    """
    Return dict with PDF-metadata

    :rtype: dict[str, str | int] | str
    :param path: 
    :return: 
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
        #debug
        print(f"meta :\n {meta}")
        meta_pdf = pdf.metadata
        print(f"meta_pdf :\n {meta_pdf}")

        if meta_pdf:
            meta.update(meta_pdf)
            meta['CreationDate'] = parse_meta_datatime(meta['CreationDate'])
            meta['ModDate'] = parse_meta_datatime(meta['ModDate'])
            return meta
        else:
            if __name__ == "__main__":
                return f"No metadata in PDF-file."
            else:
                return meta

def get_pdf_text(path:str):
    """
    Return PDF content in text mode format's
    :rtype: str | Any
    :param path: 
    :return: PDF text
    """
    try:
        with pdfplumber.open(path) as pdf:
            text = ''
            for page in pdf.pages:
                # text extract
                text += page.extract_text()
        return text
    except Exception as e:
        if __name__ == "__main__":
            return f"Error when receiving the metadata of the PDF-file: {e}"
        else:
            return f'Failed to get ...'

if __name__ == "__main__":
    #print(f"Local host name: {get_local_hostname()}")
    '''
    CreationDate = "D:20120320133836+08'00'"
    ModDate = "D:20120327142152+08'00'"
    print(parse_meta_datatime(CreationDate))
    print(parse_meta_datatime(ModDate))
    print(parse_meta_datatime(''))
    '''

    pfile = 'data/APC_Delta_manual.pdf'
    print(f"meta othe func :\n {get_pdf_meta(pfile)}")
