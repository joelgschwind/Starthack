from PIL import Image
import requests
from io import BytesIO
from distutils.version import StrictVersion
import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile

from object_detection.utils import label_map_util

from object_detection.utils import visualization_utils as vis_util

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image



# This is needed since the notebook is stored in the object_detection folder.
# sys.path.append("..")
from object_detection.utils import ops as utils_ops



def getURL(x, y):
	return 'http://maps.google.com/maps/api/staticmap?center=' + str(y) + ',' + str(x) + '&zoom=19&size=640x480&scale=2&maptype=satellite&key=AIzaSyDvh2Ss2GMSmLlUQ3O_t-uytTY0pyfw8wA'

def saveSquare(x,y):
			response =requests.get(getURL(x,y))
			img = Image.open(BytesIO(response.content))
			imgName = str(x).replace('.','') + str(y).replace('.','') + '.png'
			img.save(imgName)
			return(imgName)

def cwClassificaiton(x,y):
	imgName = saveSquare(x,y)




