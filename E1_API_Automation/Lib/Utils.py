from html.parser import HTMLParser

tagstack = []
datatag = []


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        tagstack.append(tag)

    def handle_endtag(self, tag):
        tagstack.pop()

    def handle_data(self, data):
        if data.strip():
            tagpath = ''
            for tag in tagstack:
                tagpath = tagpath + '/' + tag
            datatag.append({tagpath: data.strip()})


def get_html_tagvalues(source, tagpath):
    parser = MyHTMLParser()
    parser.feed(source)
    userdata = []

    for item in datatag:
        for key, value in item.items():
            if key == tagpath:
                userdata.append(value)
    datatag.clear()
    return userdata


def open_anything(source):
    if hasattr(source, "read"):
        return source

    if source == "-":
        import sys
        return sys.stdin

    # try to open with urllib (if source is http, ftp, or file URL)
    import urllib.request, urllib.parse, urllib.error
    try:
        return urllib.request.urlopen(source)
    except Exception:
        pass

    # try to open with native open function (if source is pathname)
    try:
        return open(source)
    except Exception:
        pass

    # treat source as string
    import io
    return io.StringIO(str(source))
