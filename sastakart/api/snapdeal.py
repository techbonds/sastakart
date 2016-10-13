from urllib2 import urlopen,Request
from bs4 import BeautifulSoup
import pprint
#  import tablib
import json
from sys import argv
from urlparse import urlparse
import HTMLParser
base_url="http://www.snapdeal.com/product/scholl-velvet-smooth-electronic-foot/763533880"
bad_url="http://www.snapdeal.com/product/apple-iphone-6-16-gb/1270529654"
good_url="http://www.snapdeal.com/product/dettol-cool-body-wash/686655750277"
alienware_url="http://www.snapdeal.com/product/dell-alienware-17-w560905in9-laptop/1728031858"

class snapdeal:
	max_attempts=0
	def __init__(self):
		pass

	def product_details(self,url):
		# print "SNAPDEAL...product_details"
		product={}
		request= Request(url)
		request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117')
		html=urlopen(request,timeout=10).read()
		soup=BeautifulSoup(html,"lxml")
		r= soup.find(id="productOverview")
		r1= r.find("div","left-card-height-cache")
		r2=r.find("div","right-card-zoom")
		# r3=r.find("div",{"class":"col-xs-4 posAbsolute"})
		# print r1
		# r11=r1.div.div.find("div",{"class":"pdp-fashion-topleft-inner pdp-left-common-container"})
		r11=r1.div.div.find_all("div")[0]
		images=0
		rating="0"
		r12=r11.find("div",{"class":"left-panel-carousel"}).find_all("div")
		for x in range(0,len(r12)):
			if(r12[x].find("div",{"id":"bx-pager-left-image-panel"})):
				images=len(r12[x].find("div",{"id":"bx-pager-left-image-panel"}).find_all("a"))
		# print "No. of images: "+str(images)
		r21=r2.div.div.find("div",{"class":"pdp-e-i-ratereviewQA"})
		try:
			rating=r21.find("div",{"class":"pdp-e-i-ratings"}).div['ratings']
			rcount=r21.find("div",{"class":"pdp-e-i-ratings"}).div.find("span",{"class":"ratings-wrapper"}).a.text.strip()[:-8]
			# rating+=" , "+rcount
		except KeyError:
			rating="0"
		# print "Rating: "+rating
		reviews=r21.find("div",{"class":"remove-underline pdp-e-i-reviews"}).div.a.text.strip()[:-44]
		# print "No. of reviews: "+reviews
		r22= r2.find("div",{"id":"buyPriceBox"})
		mrp=r22.find("div").find("div",{"class":"col-xs-8 pdp-e-i-MRP-r"}).s.span.text.strip()
		mrp=''.join(mrp.split(','))
		bb_price = r22.find("div",{"class": "row pdp-e-i-PAY"}).find("div", "pdp-e-i-PAY-r").span.span.text.strip()
		bb_price=''.join(bb_price.split(','))
		# print "Price: "+bb_price
		# print "MRP: "+mrp		
		r3=soup.find("div","product-detail-card-left")
		r33=r3.find("section",attrs={"id":"pdp-section product-specs"})
		r31=r3.find_all("div",{"class":"spec-section expanded"})
		r32=r31[len(r31)-1]
		try:
			description=r32.find("div",{"class":"spec-body"}).find("div",{"itemprop":"description"}).text.strip()
			# print description.encode(encoding='UTF-8',errors='strict')
			product['description']=description	
		except AttributeError:
			product['description']=None
		product['mrp']=mrp
		product['price']=bb_price
		product['reviews']=reviews
		product['images']=images
		product['rating']=rating
		# print "....Done"
		return product

	def offer_listing(self,url):
		try:
			# print "SNAPDEAL...offer_listing"
			offers=[]
			url_ref="http://"+urlparse(url).netloc+"/viewAllSellers"+urlparse(url).path
			request= Request(url_ref)
			request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117')
			html=urlopen(request,timeout=10).read()
			soup=BeautifulSoup(html,"lxml")
			r1=soup.find(id="allSellersWrap")
			r2=r1.find_all("section",{"class":"all-sellers-section"})
			r3=r2[len(r2)-1].div.find("div",{"class":"seller-list-wrp"}).find("div",{"class":"seller-list-ctr"})
			r4=r3.ul.find_all("li",{"class":"seller-dtls"})
			for x in range(0,len(r4)):
				r5=r4[x].div.find_all("div","seller-dtl-blk")
				offer={}
				name= r5[1].find("div","seller-nm").a.text.strip()
				price= r5[3].find("div",{"class":"price-dtls"}).find("p",{"class":"pdp-e-i-FINAL"}).text.strip()
				price=price.replace(" ","")[5:-2]
				price=''.join(price.split(','))
				offer['seller']=name
				offer['price']=price
				offers.append(offer)
				# print name
				# print price
			# print "....Done"
			return offers
		except:
			pass
			
	def search_api(self,keyword):
		surl='https://mobileapi.snapdeal.com/service/get/search/getSearchResults?apiKey=snapdeal&categoryId=0&categoryXPath=ALL&keyword=%s&number=10&start=0' % keyword
		search_results=[]
		request = Request(surl.replace(' ','%20'))
		html=urlopen(request).read()
		# decompressed_data=zlib.decompress(html, 16+zlib.MAX_WBITS)
		# print html
		html_json=json.loads(html)
		for product in html_json['searchResultDTOMobile']['catalogSearchDTOMobile']:
			sr={}
			sr['name'] = product['title'].strip()
			sr['url'] = 'http://snapdeal.com/' + product['pageUrl'].strip()
			search_results.append(sr)
		return search_results			

# s= snapdeal()
# s.product_details(bad_url)
# s.offer_listing(alienware_url)
# print s.search_api('dell')