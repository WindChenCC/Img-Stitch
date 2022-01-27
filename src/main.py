from GUI import GUIWindow

import sys
import os
import gettext
import locale

if __name__ == '__main__':
    if getattr(sys, 'frozen', None):
        root_dir = sys._MEIPASS
    else:
        root_dir = os.path.dirname(__file__)

    language, encoding = locale.getdefaultlocale()
    lang = 'zh' if 'zh' in language else 'en'

    gettext.translation(lang, os.path.join(root_dir, 'locales'), languages=[lang]).install()

    out_dir = './output'
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    GUIWindow().show()
