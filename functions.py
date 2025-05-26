import socket
import pdfplumber

def get_local_hostname():
    try:
        # get host domain name
        hostname = socket.gethostname()
        return hostname
    except Exception as e:
        if __name__ == "__main__":
            return f"Error when receiving the name of the host: {e}"
        else:
            return f'error: {e}'

def parse_meta_data():
    pass

def get_pdf_meta(path):
    try:
        meta = pdfplumber.open(path).metadata
        if not meta['Author']:
            meta['Author']=''
            if not meta['Creator']:
                meta['Creator'] = ''
        return meta
    except Exception as e:
        if __name__ == "__main__":
            return f"Error when receiving the metadata of the PDF-file: {e}"
        else:
            return f'error: {e}'

if __name__ == "__main__":

    print(f"Local host name: {get_local_hostname()}")

    PDFFILE = 'data/ПМУК-2_02-015_от_09.02.2024_О_проведении_внутренних_аудитов_функционирования_СУОТ_и_ПБ_(13538500_v2).PDF'
    meta = get_pdf_meta(PDFFILE)
    print(meta)
