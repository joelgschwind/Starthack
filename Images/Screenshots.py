from selenium import webdriver

def getUrl(x, y):
	return 'https://map.geo.admin.ch/?lang=de&topic=ech&bgLayer=ch.swisstopo.swissimage&layers=ch.swisstopo.zeitreihen,ch.bfs.gebaeude_wohnungs_register,ch.bav.haltestellen-oev,ch.swisstopo.swisstlm3d-wanderwege&layers_visibility=false,false,false,false&layers_timestamp=18641231,,,&E=' + str(x) +'&N=' + str(y) + '1194624.79&zoom=51000'

driver = webdriver.Chrome(executable_path="E:\\chromedriver_win32\\chromedriver.exe")

x = 2746132.94
y = 1256320.99
while(x < 2747836.06):
	while(y < 1254960.52):
		browser.get(getUrl(x,y))
		browser.save_screenshot(str(x).replace('.','') + str(y).replace('.','') + '.jpg')
		browser.quit()
		x += 175
		y += 75
