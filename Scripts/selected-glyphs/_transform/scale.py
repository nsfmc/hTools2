# [h] scale glyphs dialog

# reload when debugging

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs
    reload(hTools2.dialogs)

# import

from hTools2.dialogs import scaleGlyphsDialog

# run

scaleGlyphsDialog()
