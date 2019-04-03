#!/usr/bin/env ipython3

import os, sys, fnmatch

PREVIEWDIR = './Previews/'
PRESIZE = 150
PRECOLS = 6

# Find XCF files that do not yet have a PNG preview
files    = [r+os.sep+f for r,_,fs in os.walk(".") for f in fnmatch.filter(fs,'*.xcf')]
outfiles = [f+'.png' for f in files]
rebuild  = [f for f,o in zip(files,outfiles) if not os.path.isfile(o)]

# Create PNG previews of XCF files
for f in rebuild:
    print(f)
    cmd = 'xcf2png -f "%s" -o "%s.png"'%(f,f)
    os.system(cmd)
    
# Generate small PNG previews of images
files = [r+os.sep+f for r,_,fs in os.walk(".") for f in fnmatch.filter(fs,'*.png') if not r=='./Previews']

# Generates a condensed filename
def previewname(f):
    safe='qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
    savename = '_'.join(''.join([c if c in safe else ' ' for c in f]).split())
    savename = savename[:-4]+'_preview.png'
    outpath  = PREVIEWDIR+savename
    return outpath

# Build scaled-down previews of all PNG files
for f in files:
    outpath = previewname(f)
    if not os.path.isfile(outpath):
        print(outpath)
        cmd = 'convert -resize x300 "%s" "%s"'%(f,outpath)
        os.system(cmd)
        
#Generate some sort of preview HTLM document

template = '''
<html>
<head>
<style>
.crop { max-width: %(PRESIZE)dpx; overflow: hidden; }
.crop img { max-width: initial; /* Maybe optional. See note below */ }
</style>
</head>
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
<div class="crop">
<center>
<a href="../%(link)s">
<img src="../%(f)s" height="%(PRESIZE)d">
</a>
</center>
</div>
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
htmloutfile = PREVIEWDIR+'index.html'
with open(htmloutfile,'w') as f:
    f.write(HTML)

