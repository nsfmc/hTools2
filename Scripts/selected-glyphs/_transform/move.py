# [h] move glyphs dialog

'''Move contours in selected glyphs by a given distance.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs
    reload(hTools2.dialogs)

# import

from hTools2.dialogs import moveGlyphsDialog

# run

moveGlyphsDialog()
