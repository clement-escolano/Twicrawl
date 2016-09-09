from urllib.request import urlopen
from html5lib import parse
from ClassificationAlgorithms.Dictionary import Dictionary


def get_tag(element):
    return element.tag[30:]


def get_children_with_tag(element, tag):
    children = []
    for child in element:
        if get_tag(child) == tag:
            children.append(child)
    return children


def get_children_with_tags(element, tags):
    elements = [element]
    for tag in tags:
        new = []
        for el in elements:
            new.extend(get_children_with_tag(el, tag))
        elements = new
    return elements


def get_terms_from_url(url, tags):
    print("Fetching : " + url)
    page = urlopen(url)
    document = parse(page, transport_encoding=page.info().get_content_charset(), treebuilder='lxml')
    print("Fetched : " + url)
    root = document.getroot()
    elements = get_children_with_tags(root, tags)
    print(str(len(elements)) + " found with tags : " + str(tags))
    terms = []
    for element in elements:
        terms.extend(element.text.lower().split(' '))
    terms = list(set(terms))
    print(str(len(terms)) + " words in the dictionary")
    return terms


def create_dictionary_from_url(dictionary):
    urls = ["http://www.computerhope.com/vdef.htm", "http://www.computerhope.com/jargon/software.htm"]
    tags = ['body', 'div', 'section', 'article', 'table', 'tbody', 'tr', 'td', 'p', 'a']
    for url in urls:
        dictionary.register_words(get_terms_from_url(url, tags))


def create_dictionary_from_file(dictionary):
    dictionary.restore_dictionary(filename="dictionary.pkl")

dictionary = Dictionary()
create_dictionary_from_url(dictionary)
dictionary.save_dictionary()
