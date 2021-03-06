# [h] html documentation builder

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:

    import hsettings
    reload(hsettings)

    import hTools2.modules.fileutils
    reload(hTools2.modules.fileutils)

    import hTools2.modules.sysutils
    reload(hTools2.modules.sysutils)

    import hTools2.modules.ftp
    reload(hTools2.modules.ftp)

# imports

import os
import codecs
import time

try:
    import markdown
except:
    # print 'markdown not available in this enviroment.\n'
    pass

from hsettings import hSettings
from hTools2.modules.ftp import *

# object

class hDocs:

    '''An object to generate html/css/js documentation pages from markdown sources.'''

    # doct_tree = OrderedDict(
    #
    #     'section 1' : {
    #         'menu name 1' : 'path-to-file-1',
    #         'menu name 2' : 'path-to-file-2',
    #     },
    #
    #     'section 2' : {
    #         'menu name 1' : 'path-to-file-1',
    #         'menu name 2' : 'path-to-file-2',
    #     },
    #   )

    title = None
    index = {}
    index_order = []

    folders = {}
    paths = {}

    html = u''

    include_css = True
    include_js = True

    css_files = [ 'base.css', 'colors.css', 'layout.css' ]

    def __init__(self, title):
        # self.settings = hSettings()
        self.title = title

    # build

    def build(self, index, index_order, folders_dict):
        print 'building documentation...',
        self.index = index
        self.index_order = index_order
        self.build_paths(folders_dict)
        self.build_html()
        self.save_html()
        print 'done.'

    def build_paths(self, folders_dict):
        self.folders = folders_dict
        self.paths = {}
        self.paths['html'] = os.path.join(self.folders['root'], self.folders['html'])
        self.paths['css'] = os.path.join(self.folders['root'], self.folders['css'])
        self.paths['markdown'] = os.path.join(self.folders['root'], self.folders['markdown'])
        self.paths['images'] = os.path.join(self.folders['root'], self.folders['images'])

    def build_html(self):
        self.html = u''
        self.html += '<!DOCTYPE html>\n'
        self.html += '<html lang="en">\n'
        self.html += '<meta charset="utf-8" />\n'
        self.build_head()
        self.html += '<body>\n'
        # nav / content
        self.build_nav()
        self.build_content()
        self.html += '</body>\n'
        self.html += '</html>\n'

    def build_head(self):
        _html = u''
        _html += '<head>\n'
        _html += '<title>%s</title>\n' % self.title
        # include JS
        if self.include_js:
            _html += '<!-- %s -->\n' % 'JS'
            _html += '<script src="http://code.jquery.com/jquery-latest.min.js"></script>\n'
            _html += '<script src="../_js/scroll.js"></script>\n'
        # include CSS
        if self.include_css:
            _html += '<!-- %s -->\n' % 'CSS'
            _html += '<link href="../_css/base.css" rel="stylesheet" />\n'
            _html += '<link href="../_css/colors.css" rel="stylesheet" />\n'
            _html += '<link href="../_css/layout.css" rel="stylesheet" />\n'
        # done
        _html += '</head>\n'
        self.html += _html

    def build_nav(self):
        _html = u''
        _html += '<!-- %s -->\n' % 'navigation'
        _html += '<div id="nav">\n'
        # add main title
        _custom_header_path = os.path.join(self.paths['markdown'], 'header.md')
        if os.path.exists(_custom_header_path):
            _md_file = codecs.open(_custom_header_path, mode="r", encoding="utf-8")
            _title = _md_file.readline()
            _html += '<h1><a href="#top">%s</a></h1>\n' % _title
        else:
            _html += '<h1><a href="#top">%s</a></h1>\n' % self.title
        # add build time
        _time_stamp = time.strftime("%H:%M:%S %a, %d %b %Y", time.gmtime())
        _html += '<p class="timestamp">last update: %s</p>\n' % _time_stamp
        _html += '<div>\n'
        _col_depth = 2
        _count = 0
        for section in self.index_order:
            _section_path = os.path.join(self.paths['markdown'], section)
            # break into 2 columns
            if _count == _col_depth:
                _html += '</div>\n'
                _html += '<div>\n'
                _count = 0
            _html += '<h4>%s</h4>\n' % section
            _html += '<ul id="%s">\n' % section
            for item in self.index[section]:
                _item_path = os.path.join(_section_path, item + '.md')
                if os.path.exists(_item_path):
                    _md_file = codecs.open(_item_path, mode="r", encoding="utf-8")
                    _title = _md_file.readline()
                    _title = _title[3:-1]
                    _title = _title.lower()
                    _anchor = '%s_%s' % (section, _title.replace(' ', "_"))
                    _html += '<li><a href="#%s">%s</a></li>\n' % (_anchor, _title)
            _html += '</ul>\n'
            _count += 1
        _html += '</div>\n'
        _html += '</div>\n'
        self.html += _html

    def build_content(self):
        _html = u''
        _html += '<!-- %s -->\n' % 'content'
        _html += '<div id="content">\n'
        _html += '<a name="top"></a>\n'
        for section in self.index_order:
            _section_path = os.path.join(self.paths['markdown'], section)
            for item in self.index[section]:
                _item_path = os.path.join(_section_path, item + '.md')
                if os.path.exists(_item_path):
                    _md_file = codecs.open(_item_path, mode="r", encoding="utf-8")
                    _md_text = _md_file.read()
                    _html_text = markdown.markdown(_md_text)
                    _anchor = item.lower()
                    _anchor = '%s_%s' % (section, _anchor.replace(' ', "_"))
                    _html += '<a name="%s"></a>\n' % _anchor
                    _html += _html_text
        _html += '</div>\n'
        self.html += _html

    # save and upload

    def save_html(self):
        _file_name = 'index.html'
        _html_path = os.path.join(self.paths['html'], _file_name)
        _html_file = codecs.open(_html_path, "w", encoding="utf-8", errors="xmlcharrefreplace")
        _html_file.write(self.html)
        _html_file.close()

    def upload_html(self, s, ftp_dict):
        _html_folder_ftp = os.path.join(self.folders['ftp'], self.folders['html'])
        _html_file_name = 'index.html'
        _html_path = os.path.join(self.paths['html'], _html_file_name)
        F = connect_to_server(s.hDict['ftp']['url'], s.hDict['ftp']['login'], s.hDict['ftp']['password'], _html_folder_ftp, verbose=False)
        upload_file(_html_path, F)
        F.quit()

    def upload_css(self, s, ftp_dict):
        _css_folder_ftp = os.path.join(self.folders['ftp'], self.folders['css'])
        F = connect_to_server(ftp_dict['url'], ftp_dict['login'], ftp_dict['password'], _css_folder_ftp, verbose=False)
        for _css_file_name in self.css_files:
            _css_path = os.path.join(self.paths['css'], _css_file_name)
            upload_file(_css_path, F)
        F.quit()

    def upload(self, ftp_dict):
        '''Upload documentation files to ftp server.'''
        print 'uploading files to ftp server...',
        s = hSettings()
        self.upload_html(s, ftp_dict)
        self.upload_css(s, ftp_dict)
        # done
        print 'done.'
