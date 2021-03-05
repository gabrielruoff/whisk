# whisk
 
Usage:

from whisk.whisk import whisk

w = whisk()
w.sethtmldir('X:\\docker\\data\\www\\html\\')
w.settemplatedir('X:\\docker\\data\\phplib\\sitebuilder templates\\')
w.setbackupdir('backup')

w.build(backup=True)
