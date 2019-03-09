from PIL import Image
import os 
from os import listdir
from os.path import isfile

mypath = '.'

files = [f for f in os.listdir(mypath) if os.path.isfile(f)]
for f in files:
    im = Image.open(f)
    rgb_im = im.convert('RGB')
    rgb_im.save(f[0:f.index('.')] +'.jpg')
    print(".")