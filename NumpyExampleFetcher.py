"""This module retrieves the Numpy examples page from 

    http://www.scipy.org/Numpy_Example_List

parses the data a bit, and provides a simple interface to query for
various bits of example info.

Expected usage is:

    from NumpyExamples import examples
    examples('fft')

But it can also be called as a script from the command line:

    python NumpyExamples fft arccos dot

(The command line usage is not really recommended, though, because it
re-downloads the examples page every time you call it.  Caching to a
local file is not currently supported.)

You can also create your own instance of the NumpyExamples object if
you feel like it

Author: Bill Baxter
Date of creation: March 19 2007
version: 0.1
License: public domain
"""
import urllib2, re

#--- MODULE GLOBALS ---

DEFAULT_URL = 'http://www.scipy.org/Numpy_Example_List?action=raw'

default_getter = None

#--- IMPLEMENTATION ---

class NumpyExamples:
    '''Object that can download and parse examples from the Numpy examples wiki page.
    The url used defaults to 'http://www.scipy.org/Numpy_Example_List?action=raw'
    '''
    def __init__(self, url=DEFAULT_URL,comments=True, fixcomments=True):
        # try to read the target HTML document
        try:
            # TODO: cache the file on disk somewhere
            conn = urllib2.urlopen(url)
            self.fulltext = conn.read()
        except:
            raise ValueError('Could not fetch Numpy example list wiki page')
        # reset our parser and try to parse the newly fetched examples
        #print self.text
        self.comments = comments
        self.fixcomments = fixcomments
        self.example_dict = self.parse_examples(self.fulltext)


    def parse_examples(self, text):
        """Parse the text of the examples web page into a dict of
           mapping command names to the example text.
        """
        # strip the PRE {{{ type  tags from the example code
        text = re.sub(r'(\{\{\{.*)|\}\}\}', '', text)

        # fix the see also lines
        #re_seealso = re.compile(r'(See\s+also\s*:.*)$',re.IGNORECASE)
        re_seealso = re.compile(r'See\s*(also)?\s*(:)?[^[]*\[.*')
        def seealso_sub(matchobj):
            ret= munge_see_also(matchobj.group(0))
            return ret
        text = re_seealso.sub(seealso_sub, text)

        # Now split the examples based on headers that look like this:
        #   [[Anchor(broadcast)]]
        #   === broadcast() ===
        # Pick out both flavors of the name to use as keys 
        # (sometimes they're different)

        re_header = re.compile(r'\[\[\s*Anchor\s*\((\w+)\)\s*\]\]\s*'+
                               r'===\s*([^( ]+).*$',re.MULTILINE)
        all = re_header.split(text)

        alliter = iter(all)
        alliter.next() # discard first chunk, which is a header
        ret = dict()
        re_blanks = re.compile(r'^\s*$',re.MULTILINE)
        try:
            while True:
                k1  = alliter.next()
                k2  = alliter.next()
                txt = alliter.next()
                # replace multiple blank lines with just one
                txt = re_blanks.sub('', txt)
                ret[k1] = txt
                if k1 != k2:
                    ret[k2] = txt
        except StopIteration:
            pass
        return ret

    def get_example(self, name, comments=None, fixcomments=None):
        """Retrieve the examples for the given Numpy function.

        If comments is True
            leave comments in the example code
        elif comments is False
            then strip comments from the example code
        else:
            use default behavior of self.comments (no stripping)

        fixcomments is intended for reflowing comments to a width 
        more appropriate for a tty.  Set to True/False to turn it on or off.
        None gets default behavior.
        """
        # Try to convert a non str argument to something useful
        if type(name) is not type(str):
            if hasattr(name,'__name__'):
                name = name.__name__
            else:
                name = str(name)
        if name.startswith('numpy.'):
            ## Maybe this isn't needed, but fft for instance
            ## is a module name, so it's likely that get_example(fft)
            ## look for 'numpy.fft' instead of 'fft'
            name = name.replace('numpy.','')

        text = self.example_dict.get(name)
        if text is None:
            return "<No example available>"

        # strip comments conditionally
        comments_off = (comments is False) or (comments is None and self.comments is False)
        fix_on = not comments_off and (fixcomments or self.fixcomments)
        if comments_off:
            text = re.sub(r'#.*', '', text)

        def comment_fixer(mobj):
            return "\n  "+mobj.group(1)
        if fix_on:
            # TODO: the idea here is to reflow comments to a more sane 
            # width for a tty somehow
            text = re.sub(r'\s*(#.*)', comment_fixer, text)

        # strip all trailing whitespace
        text = re.sub(r'\s*$', '', text)

        return text


def munge_see_also(line):
    """This parses and re-formats a 'see also' information line from the 
    Numpy examples page.  These lines take the form:

        See also: [#bbracket []] [#dots ...], [#newaxis newaxis], [#ix_ ix_]'

    And the generated output from that looks like:

        See also: bbracket ([]), dots (...), newaxis, ix_
    """

    # A simple regexp won't work here, mainly because of the nested []
    # used inside the bbracket see also.
    # It's also nice to be able to remove duplicates.

    import shlex;

    parser = shlex.shlex(line)
    parser.commenters = []
    out = 'See also: '
    in_alt = False
    def add_char(txt,c,_in_alt):
        if not _in_alt:
            return (txt+' ('+c,True)
        return (txt+c,_in_alt)

    def parse_one(p):
        in_alt = False
        txt = ""
        blevel = 1
        after_pound = 'notyet'
        while True:
            t = p.get_token()
            if t==p.eof:
                break
            if after_pound=='notyet' and t=='#':
                after_pound = 'justgot'
                continue

            if after_pound=='justgot':
                txt = t
                after_pound='pastanchor'
                continue

            if after_pound=='pastanchor':
                if t==']':
                    blevel -= 1
                    if blevel==0:
                        break
                    else:
                        txt,in_alt = add_char(txt,t,in_alt)
                elif t=='[':
                    blevel += 1
                    txt,in_alt = add_char(txt,t,in_alt)
                elif t != txt:
                    txt,in_alt = add_char(txt,t,in_alt)
                elif t==p.eof:
                    break

        if in_alt: txt+=")"
        return txt

    toks = []
    while True:
        t = parser.get_token()
        if t=='[':
            toks.append(parse_one(parser))
        elif t==parser.eof:
            break
    out += ", ".join(toks)
    return out



#--- CONVENIENCE FUNCTION ---
def examples(name=None,comments=None,fixcomments=None):
    """Retrieve the examples for the given Numpy function.

    If comments is True
        leave comments in the example code
    elif comments is False
        then strip comments from the example code
    else:
        use default behavior (no stripping)

    fixcomments is intended for reflowing comments to a width 
    more appropriate for a tty.  Set to True/False to turn it on or off.
    None gets default behavior.

    If name is None then it will print out a list of all known commands.
    """
    global default_getter
    if default_getter is None:
        default_getter = NumpyExamples()

    if name is None:
        print "--- Known commands ---"
        k = default_getter.example_dict.keys()
        k.sort()
        print ", ".join(k)
        return

    if type(name) is not type(str):
        if hasattr(name,'__name__'):
            name = name.__name__
        else:
            name = str(name)

    print "---", name, "---"
    print default_getter.get_example(name,comments,fixcomments)


#--- SCRIPT CALL INTERFACE ---
if __name__ == '__main__':
    import sys,os
    if len(sys.argv)==1:
        print "Looks up usage examples for Numpy functions from the Numpy examples page at"
        print "  ",  DEFAULT_URL.split('?')[0]
        print "Usage: python", sys.argv[0].split(os.sep)[-1], "<commands>"
    else:
        for a in sys.argv[1:]:
            examples(a)
            