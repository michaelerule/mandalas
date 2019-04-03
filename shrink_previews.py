#!/usr/bin/env ipython3

import os, sys, fnmatch

PREVIEWDIR = './Previews/'
PRESIZE = 150
PRECOLS = 6

previews = [PREVIEWDIR+f for f in os.listdir(PREVIEWDIR) if '.png' in f]

for f in previews:
    print(f)
    cmd = 'convert -resize x300 "%s" "%s"'%(f,f)
    os.system(cmd)
