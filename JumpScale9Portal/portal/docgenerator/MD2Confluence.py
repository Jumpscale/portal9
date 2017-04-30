from js9 import j


import re
import os
import sys


class Image(object):

    def __init__(self, line):
        self.regex = '\!\[([\w\-_\s]*)\]'
        self.line = line
        self._exists = False
        self._alt = ''

    def parse(self):
        if self.line:
            m = re.search(self.regex, self.line)
            if m:
                try:
                    self._alt = m.group(1)
                    self._exists = True
                except IndexError:
                    pass

    @property
    def exists(self):
        return self._exists

    @property
    def alt(self):
        return self._alt

    @property
    def wiki(self):
        return '!%s!' % self.url

    @property
    def url(self):
        newline = self.line.split('![%s]' % self.alt)[1]
        if newline.startswith('('):
            return newline.split(')')[0][1:]


class HorizontalLine(object):

    def __init__(self, line):
        self.regex = '^([\*-]\s*)+$'
        self.line = line
        self._exists = False

    def parse(self):
        if self.line and re.search(self.regex, self.line):
            self._exists = True

    @property
    def wiki(self):
        return '{{html:<hr/>}}'

    @property
    def exists(self):
        return self._exists


class OrderedList(object):
    """
    One level for now
    """

    def __init__(self, line, **kwargs):
        self.line = line.strip()
        self._lines = kwargs.get('lines')
        self._curridx = kwargs.get('currentidx')
        self._newcontent = kwargs.get('newContent')
        self._orderedlist = []

    def parse(self):
        while self.line.startswith('-'):
            self._orderedlist.insert(0, self.line[:])
            if self._lines[self._curridx - 1].strip().startswith('-'):
                self.line = self._lines[self._curridx - 1].strip()
                self._curridx = self._curridx - 1
                self._newcontent.pop()
            else:
                self.line = ''

    @property
    def exists(self):
        return bool(self._orderedlist)

    @property
    def wiki(self):
        ret = ''
        for element in self._orderedlist:
            ret += '*# %s \n' % element.replace('-', '')
        return ret


class URL(object):

    def __init__(self, line):
        self.regex = '\[([\w\-_:\/.*\s]*)\]'
        self.line = line
        self._exists = False
        self._alt = ''

    def parse(self):
        if self.line:
            m = re.search(self.regex, self.line)
            if m and '!' not in self.line:
                try:
                    self._alt = m.group(1)
                    self._exists = True
                except IndexError:
                    pass

    @property
    def exists(self):
        return self._exists

    @property
    def alt(self):
        return self._alt

    @property
    def wiki(self):
        u = '[%s' % self._alt
        u += '|%s' % self.url if self.url else ''
        u += ']'
        return u

    @property
    def url(self):
        newline = self.line.split('[%s]' % self.alt)[1]
        if newline.startswith('('):
            return newline.split(')')[0][1:]


class Header(object):

    def __init__(self, line, **kwargs):
        self._exists = False
        self.line = line
        self._wiki = ''
        self._lines = kwargs.get('lines')
        self._curridx = kwargs.get('currentidx')
        self._newcontent = kwargs.get('newContent')

    def _remove_previous_line(self):
        self._newcontent.pop()

    def parse(self):
        self._exists = True
        if self.line.startswith('######'):
            self._wiki = 'h6. %s' % self.line.replace('######', '')
        elif self.line.startswith('#####'):
            self._wiki = 'h5. %s' % self.line.replace('#####', '')
        elif self.line.startswith('####'):
            self._wiki = 'h4. %s' % self.line.replace('####', '')
        elif self.line.startswith('###'):
            self._wiki = 'h3. %s' % self.line.replace('###', '')
        elif self.line.startswith('##'):
            self._wiki = 'h2. %s' % self.line.replace('##', '')
        elif self.line.startswith('#'):
            self._wiki = 'h1. %s' % self.line.replace('#', '')
        elif self.line.startswith('='):
            self._wiki = 'h1. %s' % self._lines[self._curridx - 1]
            self._remove_previous_line()
        elif self.line.startswith('--'):
            self._wiki = '%s' % self._lines[self._curridx]
        else:
            self._exists = False

    @property
    def exists(self):
        return self._exists

    @property
    def wiki(self):
        return self._wiki


class TableElement(object):

    def __init__(self, line, **kwargs):
        self.line = line
        self._exists = False
        self._header = ''
        self._row = ''
        self._lines = kwargs.get('lines')
        self._curridx = kwargs.get('currentidx')
        self._wiki = ''
        self._newcontent = kwargs.get('newContent')

    def _remove_previous_line(self):
        return self._newcontent.pop()

    def parse(self):
        if self.line.startswith('|'):
            self._exists = True
            if '--' in self.line:
                previousline = self._remove_previous_line()
                self._header = previousline.replace('|', '||')
            else:
                self._row = self.line

    @property
    def exists(self):
        return self._exists

    @property
    def wiki(self):
        if self._header:
            return self._header
        else:
            return self._row

    @property
    def url(self):
        newline = self.line.split('[%s]' % self.alt)[1]
        if newline.startswith('('):
            return newline.split(')')[0][1:]


class Quote(object):

    def __init__(self, line, **kwargs):
        self.line = line.strip()
        self._lines = kwargs.get('lines')
        self._curridx = kwargs.get('currentidx')
        self._newcontent = kwargs.get('newContent')
        self._quoteblock = []

    def parse(self):
        while self.line.startswith('>'):
            self._quoteblock.insert(0, self.line[:].replace('>', '').strip())
            if self._lines[self._curridx - 1].strip().startswith('>'):
                self.line = self._lines[self._curridx - 1].strip()
                self._curridx = self._curridx - 1
                self._newcontent.pop()
            else:
                self.line = ''

    @property
    def exists(self):
        return bool(self._quoteblock)

    @property
    def wiki(self):
        return '{{html:\n<blockquote>%s</blockquote>}}' % '<br/>'.join(self._quoteblock)


class MD2Confluence():

    def convert(self, c):
        # replace all links
        # c = re.sub(r'\[([^\]]+)\]\(([^\]]+)\)', r'[\1|\2]', c)
        #         c = re.sub(r'\[(.*?)\]\((.*?)\)', r'[\1|\2]', c)
        #
        #         # replace bold temporarily
        c = re.sub(r'\*\*(.*?)\*\*', r'bdirkb\1bdirkb', c)
#         # replace italics
        c = re.sub(r'\*(.*?)\*', r'_\1_', c)
#         # replace bold
        c = re.sub(r'bdirkb(.*?)bdirkb', r'*\1*', c)
#
        # code
#         c = re.sub(r'`(.*?)`', r'{{html:    <code>\1</code>}}', c)

        c = re.sub('```(.+?)```', r'{{code:\1}}', c, flags=re.DOTALL)
#         # replace inline code

        # print c
        c = c.split('\n')
        words = []
        newContent = []

        isCode = 0
        indent = 0
        isQuote = 0
        isList = 0

        for idx, l in enumerate(c):

             # Table element
            tableelement = TableElement(l, lines=c, currentidx=idx, newContent=newContent)
            tableelement.parse()
            if tableelement.exists:
                newContent.append(tableelement.wiki)
                continue

            # Headers
            header = Header(l, lines=c, currentidx=idx, newContent=newContent)
            header.parse()
            if header.exists:
                newContent.append(header.wiki)
                continue

            # URLs
            url = URL(l)
            url.parse()
            if url.exists:
                newContent.append(url.wiki)
                # remove that rendered url from line
                l = l.replace('[%s]' % url.alt, '').replace('(%s)' % url.url, '')

            # Images
            img = Image(l)
            img.parse()
            if img.exists:
                newContent.append(img.wiki)
                # remove that rendered image from line
                l = l.replace('![%s]' % img.alt, '').replace('(%s)' % img.url, '')

            # horizontal line
            hr = HorizontalLine(l)
            hr.parse()
            if hr.exists:
                newContent.append(hr.wiki)
                continue

            orderedlist = OrderedList(l, lines=c, currentidx=idx, newContent=newContent)
            orderedlist.parse()
            if orderedlist.exists:
                newContent.append(orderedlist.wiki)
                continue

            quote = Quote(l, lines=c, currentidx=idx, newContent=newContent)
            quote.parse()
            if quote.exists:
                newContent.append(quote.wiki)
                continue

#             if l.startswith('>'):
#                 newContent.append('bq. %s' % l.replace('>', ''))
#                 continue

#             if isCode == 1:
#                if l[0:1] == ' ' or l[0:1]=='\t':
#                  k = k[indent:]
#                else:
#                  k = '{code}\n'+k
#                  isCode = 0
#                  indent = -1
#             else:
#                if l[0:1]==' ' or l[0:1]=='\t':
#                  indent = len(k)-len(k.lstrip())
#                  k = '{code}\n'+k[indent:]
#                  isCode = 1

            k = l
            if l[0:1] == '*':
                isList = 1
            if l == '':
                isList = 0

            if l[0:1] == '>':
                if isQuote == 0:
                    k = 'bq. ' + k[1:]
                    isQuote = 1
                else:
                    k = k[1:]
#
#
            if isList == 0:
                pass
            else:
                if l[0:4] == '\t\t\t*':
                    k = '****' + l[4:]
                if l[0:3] == '\t\t*':
                    k = '***' + l[3:]
                if l[0:2] == '\t*':
                    k = '**' + l[2:]
#
            for w in words:
                # print l[:len(w[0])]
                if l[:len(w[0])] == w[0]:
                    k = w[1] + l[len(w[0]):]

            if l[0:3] != '| -':
                newContent.append(k)
#


#             print k
            # newContent.append(k)
        return '\n'.join(newContent)
