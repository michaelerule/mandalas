#!/usr/bin/env ipython3

import os, sys, fnmatch

PREVIEWDIR = '../Nice/'
PRESIZE = 200
PRECOLS = 3
    
# Generate small PNG previews of images
files = [r+os.sep+f for r,_,fs in os.walk("..") for f in fnmatch.filter(fs,'*.png') if not r=='../Previews']

# Generates a condensed filename
def previewname(f):
    safe='qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
    savename = '_'.join(''.join([c if c in safe else ' ' for c in f]).split())
    savename = savename[:-4]+'_preview.png'
    outpath  = PREVIEWDIR+savename
    return outpath


#Generate some sort of preview HTLM document

template = '''
<html>
<head></head>
<body>
<table>
<tr></tr>
<td></td>
%(IMAGETABLE)s
</table>
</body>
</html>
'''

imgtemplate = '''
<td>
<center>
<a href="%(link)s">
<img src="%(f)s" height="%(PRESIZE)d">
</a>
</center>
</td>
'''

# Get all files that have a valid preview image
previews = [PREVIEWDIR+f for f in os.listdir(PREVIEWDIR) if '.png' in f]
allpreviews = []
for f in files:
    pname = previewname(f)
    if pname in previews:
        allpreviews += [(f,pname)]
nfiles = len(allpreviews)
print('There are %d preview images'%nfiles)

# Show them in a random order
from random import shuffle
shuffle(allpreviews)

# Display images in a large table
IMAGETABLE = '<tr>'
nincol = 0
for link,f in allpreviews:
    imagetag = imgtemplate%globals()
    IMAGETABLE += imagetag
    nincol += 1
    if nincol>PRECOLS:
        IMAGETABLE += '</tr>\n<tr>'
        nincol=0
# Close table environment
while nincol<PRECOLS:
    IMAGETABLE += '<td></td>'
    nincol += 1
IMAGETABLE+='</tr>'

# Write out HTML file
HTML = template%globals()
print(HTML)
htmloutfile = './index.html'
with open(htmloutfile,'w') as f:
    f.write(HTML)

