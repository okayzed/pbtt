import requests
import re
from bs4 import BeautifulSoup
import StringIO

import pdf_title_extract
SUPPORTS_PDF = pdf_title_extract.SUPPORTS_PDF

def grab_url(line):
    m = re.search("(?P<url>https?://[^\s]+)", line)
    if m:
        return m.group("url")

def print_url_title(response, line, nick):
    url = grab_url(line)
    if not url:
        return

    print "RETRIEVING URL", url

    chunk_size = 8096
    body = []
    bytes = 0
    is_pdf = False
    max_bytes=1024*1024
    with requests.get(url, verify=False, stream=True) as r:
        content_type = r.headers.get('content-type')
        if r.status_code != 200:
            return

        print "CONTENT TYPE", content_type
        is_pdf = content_type.find("application/pdf") != -1 and SUPPORTS_PDF
        if is_pdf:
            max_bytes = 8 * 1024 * 1024; # up to 8MB for PDF

        for chunk in r.iter_content(chunk_size):
            bytes += len(chunk)
            body.append(chunk)
            if bytes > max_bytes:
                break

    body = "".join(body)

    if is_pdf:
        title = pdf_title_extract.get_pdf_title(body)
        if title:
            response.say("> %s" % title.encode("utf-8"))
    else:
        soup = BeautifulSoup(body, "lxml")
        if soup.title:
            title = soup.title.string.encode("utf-8")
            response.say("> %s" % title)
