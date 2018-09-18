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
    userdata.clear()
    return userdata
