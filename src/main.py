from GUI import GUIWindow

import os
import gettext
import locale

if __name__ == '__main__':
    out_dir = './output'
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    language, encoding = locale.getdefaultlocale()
    lang = 'en' if 'zh' in language else 'en'

    gettext.translation(lang, './locales', languages=[lang]).install()
    GUIWindow().show()
