import epub_conversion
from epub_conversion.utils import get_files_from_path, convert_epub_to_lines, open_book
import gzip
import re

friendimorphs_path = '/Users/averygreen/Documents/Fun/Friendimorphs/eBooks/01'
converter = epub_conversion.Converter(friendimorphs_path)

def to_raw_text(text, keep_whitespace=False, normalize_ascii=True):

    # bracket_parser = re.compile("\[\[(?P<name>[^\]\|]+)(?:\|[\W]*(?P<trigger>[^\]\#\|]+)(?:\#[^\]\|]+)?)*\]\]")
    # squiggly_bracket_parser = re.compile("{{([^}]+)}}")
    # table_parser = re.compile("{\|[^}]+\|}")
    # mvar_parser = re.compile("{{\d*mvar\d*\|([^}]+)}}")
    # remove_emphasis = re.compile("'{2,5}([^']+)'{2,5}")

    # handles links that don't have a pipe sign"
    # double_bracket_parser = re.compile("\[\[|\]\]")
    # normalizes: 01/02/2003, 2005-06-07, and 2001 type dates to 7777
    # date_remover = re.compile("((\d{4}(?:[-/]\d{2}[-/]\d{2})?)|(\d{2}(?:[-/]\d{2}[-/]\d{4})))(?=[^\d]|$)")
    # remove_emphasis_asterix = re.compile("\*{2,5}([^\*]+)\*{2,5}")
    # remove_emphasis_slash = re.compile("/{2,5}([^/]+)/{2,5}")
    # remove_emphasis_low_ticks = re.compile(",{2,5}([^,]+),{2,5}")
    # remove_emphasis_heading = re.compile("={2,5}([^=]+)={2,5}")
    # remove_emphasis_strikethrough = re.compile("~{2}([^~]+)~{2}")
    # remove_emphasis_underline = re.compile("_{2}([^_]+)_{2}")
    # remove_bullets_nbsps = re.compile(
    #     "(&amp;nbsp;|&nbsp;|[\^\n]\*{1,}|[\^\n]\#{1,}|[\^\n]:{1,})")  # remove lists, bullet points, and html no breakspace
    # remove_wikipedia_link = re.compile("\[\W*http[^\] ]+\b*(?P<anchor>[^\]]+)\]")
    # markup_normalizer = re.compile("[',/\*_=-]{2,5}")
    # markup_removes = [
    #     remove_emphasis,
    #     remove_emphasis_heading,
    #     remove_emphasis_asterix,
    #     remove_emphasis_slash,
    #     remove_emphasis_low_ticks,
    #     remove_emphasis_strikethrough,
    #     remove_emphasis_underline
    # ]
    # replacer = lambda matches: matches.group('trigger') if matches.group('trigger') != None else matches.group('name')
    # anchor_replacer = lambda matches: matches.group('anchor') if matches.group('anchor') else ''
    html_remover = re.compile("<[^>]+>")
    # internal_html_remover = re.compile("{{[^(}})]+}}")
    # math_source_sections = re.compile("<(math|source|code|sub|sup)[^>]*>([^<]"
    #                                   "*)</(math|source|code|sub|sup)>")
    # greater_than = re.compile("(\W)>(\W)")
    # less_than = re.compile("<([^\w/])")
    # single_internal_link = re.compile("\[\[([^\]\|]+)\]\]")
    # category_internal_link = re.compile("\[\[Category:([^\]\|]+)\]\]")

    # handles links that always have a pipe sign e.g. "[[the girl|Angelina Jolie]]"
    # anchortag_internal_link = re.compile("\[\[(?P<target>[^\]\|]+)\|[\W]*("
    #                                      "?P<anchor>[^\]\#\|]+)(?:\#[^\]\|]+)?\]\]")
    # url_remover = re.compile("http://[a-zA-Z\.&/]+")
    empty_space = " "
    # empty_string = ""

    # def remove_dates(text):
    #     return date_remover.sub("7777", text)
    #
    def remove_html(text):
        return html_remover.sub(empty_space, text)

    # def remove_markup(text):
    #     return markup_normalizer.sub(empty_string, text)
    #
    # def reintroduce_less_than(text):
    #     # return text
    #     # return less_than.sub("&lt;\g<1>", text)
    #     return less_than.sub("&lt;", text)
    #
    # def reintroduce_greater_than(text):
    #     # return text
    #     # return greater_than.sub("\g<1>&gt;\g<2>", text)
    #     return greater_than.sub("&gt;", text)
    #
    # def reintroduce_less_than_greater_than(text):
    #     return reintroduce_less_than(reintroduce_greater_than(text))
    #
    # def remove_math_sections(text):
    #     return math_source_sections.sub(empty_space, reintroduce_less_than_greater_than(text))
    #
    # def _remove_brackets(text):
    #     return anchortag_internal_link.sub(
    #         "\g<anchor>",
    #         single_internal_link.sub(
    #             "\g<1>",
    #             category_internal_link.sub(
    #                 "\n\g<1> .\n",
    #                 text
    #             )
    #         )
    #     )
    #
    # def _remove_table(text):
    #     return table_parser.sub(empty_space, text)
    #
    # def _remove_squiggly_bracket(text):
    #     return squiggly_bracket_parser.sub(empty_space, text)
    #
    # def _remove_mvar(text):
    #     return mvar_parser.sub("\g<1>", text)
    #
    # def remove_remaining_double_brackets(text):
    #     return double_bracket_parser.sub(empty_space, text)
    #
    # def _remove_urls(text):
    #     return url_remover.sub("url", text)
    #
    # def remove_brackets(text):
    #     return remove_remaining_double_brackets(_remove_brackets(text))

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
    # out = text
    # out = _remove_urls(text)
    # out = _remove_mvar(out)
    # out = _remove_squiggly_bracket(out)
    # out = _remove_table(out)
    # out = _remove_brackets(out)
    # out = remove_remaining_double_brackets(out)
    # out = remove_markup(out)
    # out = remove_wikipedia_link.sub(anchor_replacer, out)
    # out = remove_bullets_nbsps.sub(empty_space, out)
    # out = remove_dates(out)
    # # out = remove_math_sections(out)
    # if out != text:
    #     test = 1
    out = remove_html(text)
    out = re.sub('&gt;', '>', re.sub('&lt;', '<', out))
    out = out.lstrip()
    # out2 = sent_tokenize(out, keep_whitespace, normalize_ascii)
    # out3 = sent_tokenize(out, True, True)
    # out4 = sent_tokenize(out, False, False)
    # out5 = sent_tokenize(out, True, False)
    return out

def convert_lines_to_text(lines):
    i = 0
    for sentence in lines:
        if i == 221:
            test = 1
        raw_sentence = to_raw_text(sentence)
        if len(raw_sentence) > 0 and raw_sentence != '\r':
            try:
                # yield " ".join(raw_sentence[0])+"\n"
                yield raw_sentence
            except:
                test = 1
        i += 1

def convert(target_path):

    epub_paths = get_files_from_path(".epub", friendimorphs_path)

    with gzip.open(target_path, "wb") as file:
        for (epub_path, epub_name) in epub_paths:
            book = open_book(epub_path)
            if book is not None:
                for sentence in convert_lines_to_text(convert_epub_to_lines(book)):
                    file.write(sentence.encode("utf-8"))
                print("Wrote \"%s\" to disk" % (epub_name))
            else:
                print("Couldn't open \"%s\"." % (epub_name))

convert(friendimorphs_path + '/thing.gz')

# converter.convert("my_succinct_text_file.gz")

test = 1