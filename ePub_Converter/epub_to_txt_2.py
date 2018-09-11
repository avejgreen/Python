import epub_conversion
from epub_conversion.utils import get_files_from_path, convert_epub_to_lines, open_book
import gzip
import re
import numpy as np
import glob

friendimorphs_path = '/Users/averygreen/Documents/Fun/Friendimorphs/eBooks'
converter = epub_conversion.Converter(friendimorphs_path)

def to_raw_text(text, keep_whitespace=False, normalize_ascii=True):

    html_remover = re.compile("<[^>]+>")
    empty_space = " "

    def remove_html(text):
        if text[0:58] == '  <h4 class="calibre1"><span style="font-weight: normal;">':
            return ''
        elif text == '  <h3 class="calibre1">Table of Contents</h3>\r':
            return ''
        else:
            return html_remover.sub(empty_space, text)

    """
    A generator to convert raw text segments, with xml, and other
    non-textual content to a list of words without any markup.
    Additionally dates are replaced by `7777` for normalization.

    Arguments
    ---------
       text: str, input text to tokenize, strip of markup.
       keep_whitespace : bool, should the output retain the
          whitespace of the input (so that char offsets in the
          output correspond to those in the input).

    Returns
    -------
        generator<list<list<str>>>, a generator for sentences, with
            within each sentence a list of the words separated.
    """

    out = remove_html(text)
    out = re.sub('&gt;', '>', re.sub('&lt;', '<', out))
    out = out.lstrip()

    return out

def convert_lines_to_text(lines):
    i = 0
    for sentence in lines:
        if i == 221:
            test = 1
        raw_sentence = to_raw_text(sentence)
        if len(raw_sentence) > 0 and raw_sentence != '\r':
            try:
                yield raw_sentence
            except:
                test = 1
        i += 1


all_books = glob.glob('/Users/averygreen/Documents/Fun/Friendimorphs/eBooks/*.epub', False)



def convert(target_path, end_file):

    epub_paths = get_files_from_path(".epub", friendimorphs_path)
    epub_paths.sort()
    epub_paths = epub_paths[0:end_file]

    with gzip.open(target_path, "wb") as file:
        for (epub_path, epub_name) in epub_paths:
            book = open_book(epub_path)
            if book is not None:
                for sentence in convert_lines_to_text(convert_epub_to_lines(book)):
                    file.write(sentence.encode("utf-8"))
                print("Wrote \"%s\" to disk" % (epub_name))
                file.write('\r'.encode("utf-8"))
            else:
                print("Couldn't open \"%s\"." % (epub_name))

for book_range in range(1, 55):
    convert(friendimorphs_path + '/text_' + str(book_range) + '.gz', book_range)

test = 1