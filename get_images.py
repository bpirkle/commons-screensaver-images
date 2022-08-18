#!/usr/bin/python

# This script pulls a list of images from Wikimedia Commons and outputs
# a file containing the images that were of the desired aspect ratio.
# There's really no reason this needs to be a pywikibot script.
# I just happened to have a similar script sitting around that used
# pywikibot, so this was quick and easy.
#
# Most functions herein don't do much error handling.
# Instead, exceptions will be thrown, which is messy but effective.

import json
import pywikibot
from pywikibot.comms import http
# from pywikibot import pagegenerators, textlib

COMMONS_API_BASE_URL = 'https://commons.wikimedia.org/w/api.php'
API_QUERY_PARAMS = '?action=query&generator=categorymembers&format=json&gcmtype=file&gcmtitle=Category:Featured_pictures_on_Wikimedia_Commons&prop=imageinfo&gcmlimit=50&iiprop=url|extmetadata&iiurlwidth=1920&continue=&gcmcontinue='
OUTPUT_FILE = './screensaver-images.txt'

# ===========================================================
# retrieves the image json as a string from backstage
# ===========================================================
def fetchImagesJson(gcmcontinue):
	url = COMMONS_API_BASE_URL + API_QUERY_PARAMS + gcmcontinue
	response = http.fetch(url)
	if not response.content:
		pywikibot.output('No json content available. Quitting.')
		quit()
	return response.content

# ===========================================================
# parses the image json string into an object
# ===========================================================
def parseImagesJson(imageJson):
	return json.loads(imageJson)

# ===========================================================
# converts a single api object to wikitext
# ===========================================================
def extractImageUrls(imagesInfo):
	urls = []
	for page in imagesInfo['query']['pages'].values():
		if page['imageinfo'][0]['thumbwidth'] == 1920:
			if page['imageinfo'][0]['thumbheight'] == 1440:
				urls.append(page['imageinfo'][0]['thumburl'])
	return urls

# ===========================================================
# writes data to the output file, appending if the file already exists
# ===========================================================
def saveOutputFile(urls):
	with open(OUTPUT_FILE, 'a') as result_file:
		for url in urls:
			result_file.write(url)
			result_file.write('\n')
		result_file.close();

# ===========================================================
# main script routine
# ===========================================================
def main():
	pywikibot.output('------- begin get_images.py -------');

	gcmcontinue = ''
	count = 0
	imageUrlCount = 0;
	while imageUrlCount < 1000:
		print('iteration number ' + str(count))
		print('urls found ' + str(imageUrlCount))
		imagesJson = fetchImagesJson(gcmcontinue)
		imagesInfo = parseImagesJson(imagesJson)
		gcmcontinue = imagesInfo['continue']['gcmcontinue']
		imageUrls = extractImageUrls(imagesInfo)
		saveOutputFile(imageUrls);
		imageUrlCount += len(imageUrls)
		count += 1

	pywikibot.output('------- end get_images.py -------');

# ===========================================================
#  script entry point
# ===========================================================
main()
