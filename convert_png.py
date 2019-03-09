from PIL import Image
import glob
import os

folder = 'D:/Images2/'
imList=glob.glob(folder+'*.png')

# Loop through all the images:
for png in imList:
    # open the image
    im = Image.open(png)
    # extract the filename and extension from path
    fileName, fileExt = os.path.splitext(png)
    rgb_im = im.convert('RGB')
    # save the image in the same folder, with the same name, except *.jpg
    im.save(fileName+'.jpg')