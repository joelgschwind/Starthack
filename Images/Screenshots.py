from PIL import Image
import requests
from io import BytesIO

xStep = 0.00154
yStep = 0.00108

def getURL(x, y):
	return 'http://maps.google.com/maps/api/staticmap?center=' + str(y) + ',' + str(x) + '&zoom=19&size=640x480&scale=2&maptype=satellite&key=[YOUR_API_KEY]'

def saveSquare(xS,yS,xE, yE):
	print('Start saving square: ')
	ySTemp = yS
	while(xS < xE):
		while(yS > yE):
			response =requests.get(getURL(xS,yS))
			img = Image.open(BytesIO(response.content))
			img.save(str(xS).replace('.','') + str(yS).replace('.','') + '.png')
			yS -= yStep
			xS = round(xS, 5)
			yS = round(yS, 5)
			print('.')
		xS += xStep
		yS = ySTemp


#Zuerich
x = 8.492131
xEnd = 8.546861
y = 47.391053
yEnd = 47.367364
saveSquare(x,y,xEnd,yEnd)

#Bern
x = 7.428058
xEnd = 7.464576
y = 46.957237
yEnd = 46.939041
saveSquare(x,y,xEnd,yEnd)

#St. Gallen
x = 9.373032
xEnd = 9.398142
y = 47.434644
yEnd = 47.427160
saveSquare(x,y,xEnd,yEnd)

