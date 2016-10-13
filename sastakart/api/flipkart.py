from urllib2 import urlopen,Request
from bs4 import BeautifulSoup
import pprint
import json
from sys import argv
from urlparse import urlparse
import HTMLParser
import time
import zlib

base_url="http://www.flipkart.com/search?q=%s&as=off&as-show=on&otracker=start"

class flipkart:
	max_attempts=0
	rating="0"
	reviews="0"
	def __init__(self):
		pass

	def product_details(self,url):
		# print"FLIPKART...product_details"
		product={}
		product['offers']=[]
		images=0
		request = Request(url)
		request.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)')
		html=urlopen(request,timeout=20).read()
		soup=BeautifulSoup(html,"lxml")		
		s=soup.find("div",{"id":"fk-mainbody-id"})
		s1=s.div.find_all("div", { "class" : "gd-row" }, recursive=False)
		r1=s1[6]
		r2 =s1[7]

		r11=r1.div.find("div",{"class":"right-col-wrap lastUnit"})
		r12=r1.div.find("div",{"class":"left-col-wrap unit"})
		try:
			r155= r11.find("div",{"class":"toolbar-wrap line section"})
			r154=r155.find("div",{"class":"ratings-reviews-wrap"}) #old line
			r15= r154.find("div",{"class":"ratings-reviews line omniture-field"}) #new line to be checked
			if(r15.div):
				r151=r15.div.find("div",{"class":"ratings"})
				r152=r15.div.find("div",{"class":"reviews"})
			if(r151):
				self.rating=r151.find("div",{"class":"fk-stars"})['title'][:-6]
				# rcount=r151.find("div",{"class":"count"}).span.text.strip()
				# self.rating+=" , "+rcount
			if(r152):
				self.reviews=r152.a.span.text.strip()
		except AttributeError:
			pass
		# print "Rating: " +self.rating
		# print "Reviews: "+self.reviews
		r13=r11.div.div.find("div",{"class":"shop-section-wrap"})
		r14= r13.div.find("div",{"class": "left-section-wrap size2of5 unit"}).find("div",{"class": "prices"})
		try:
			mrp= r14.find("span", {"class":"price"}).text.strip()[4:]
			bb_price = r14.find("div").find("span",{"class": "selling-price omniture-field"}).text.strip()[4:]
		except AttributeError:
			mrp = r14.div.find("span",{"class": "selling-price omniture-field"}).text.strip()[4:]
			bb_price = mrp
		mrp=''.join(mrp.split(','))
		bb_price = ''.join(bb_price.split(','))
		# print 'MRP: '+ str(mrp)
		# print 'Price: '+ str(bb_price)		

		r16=r12.div.div.find("div",{"class":"innerPanel"}).find("div",{"class":"carouselContainer leftDisabled"})
		images=len(r16.find("ul",{"class":"carousel leftDisabled"}).find_all("li"))
		# print "No. of Images: "+ str(images)
		try:
			r21=str(r2.div.div['data-config'])
			o = json.loads(r21)
			# pp = pprint.PrettyPrinter(indent=4)
			# pp.pprint(len(o['dataModel']))  

			for x in range(0,len(o['dataModel'])):
				offer={}
				current=o['dataModel'][x]
				rating_info = current['sellerRatingInfo']
				no_of_rating=rating_info['count']
				rating= rating_info['ratingOutOfFive']
				newseller= rating_info['isNewSeller']
				seller=str(current['sellerInfo']['name']).encode("ascii","ignore")
				price= str(current['priceInfo']['sellingPrice']).encode("ascii","ignore")
				offer['seller']=seller
				offer['price']=price
				offer['rating']=rating
				offer['is_new']=newseller
				offer['rating_count']=no_of_rating
				product['offers'].append(offer)
				# print offer['seller'], offer['price'], offer['rating'], offer['is_new'], offer['rating_count']
				# print len(product['offers'])
		except TypeError:
			product['offers']= None
		product['mrp']=mrp
		product['price']= bb_price
		product['reviews']=self.reviews
		product['images']=images
		product['rating']=self.rating
		product['description'] = None
		# print "....Done"
		return product

	def get_rating(self,url):
		try:
			request = Request(url)
			request.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)')
			html=urlopen(request,timeout=10).read()
			soup=BeautifulSoup(html,"lxml")		
			s=soup.find("div",{"id":"fk-mainbody-id"})
			s1=s.div.find_all("div", { "class" : "gd-row" }, recursive=False)
			r1=s1[6]
			r11=r1.div.find("div",{"class":"right-col-wrap lastUnit"})
			r155= r11.find("div",{"class":"toolbar-wrap line section"})
			r15=r155.find("div",{"class":"ratings-reviews-wrap"})
			if(r15.div):
				r151=r15.div.find("div",{"class":"ratings"})
				r152=r15.div.find("div",{"class":"reviews"})
			if(r151):
				self.rating=r151.find("div",{"class":"fk-stars"})['title'][:-6]
				rcount=r151.find("div",{"class":"count"}).span.text.strip()
				# self.rating+=" , "+rcount
			if(r152):
				self.reviews=r152.a.span.text.strip()
		except AttributeError:
			print "error-rating (AttributeError)"
			self.get_rating(url)

	def get_desc(self,url):
		print "FLIPKART...get_desc"
		while True:
			# try:
			request = Request(url)
			request.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)')
			html=urlopen(request,timeout=100).read()
			soup1 = BeautifulSoup(html, "lxml")
			sx=soup1.find("div",{"id":"fk-mainbody-id"})
			# print sx
			s1x=sx.find_all("div",  "gd-row" )	
			# print len(s1x)	
			description=s1x[13].find_all("div")[0].find("div",{"class":"description-text"}).text.strip()
			# description=s1x[13].find_all("div")[0].find_all("div")#.find("p",{"class":"description"}).text.strip()
			# print len(description)
			print description.encode(encoding='UTF-8',errors='strict')
			print "....Done"
			return description
			# except Exception,e:
				# print "error-description"+str(e)
				# break
	
	def search_api(self,keyword):
		surl='http://mobileapi.flipkart.net/3/discover/getSearch?store=search.flipkart.com&start=0&count=10&q=' + keyword
		search_results=[]
		request = Request(surl.replace(' ','%20'))
		request.add_header('X-User-Agent','Mozilla/5.0 (Linux; Android 4.4.9; YOLO Build/P) AppleWebKit/365 (KHTML, like Gecko) Version/4.0 Chrome/11.0.0.0 Mobile Safari/364.36 FKUA/Retail//Android/Mobile (gogla/YOLO/000000000000000000000000000000)')
		request.add_header('Host','mobileapi.flipkart.net')
		request.add_header('Accept-Encoding','gzip')	
		html=urlopen(request).read()
		decompressed_data=str(zlib.decompress(html, 16+zlib.MAX_WBITS))
		decompressed_js=json.loads(decompressed_data)
		# print decompressed_data
		for prod in decompressed_js['RESPONSE']['product'].keys():
			sr={}
			product=decompressed_js['RESPONSE']['product'][prod]
			# print product[0]
			sr['name']=str(product['value']['titles']['title']).strip() + ' ' + str(product['value']['titles']['subtitle']).strip()
			sr['url']=str(product['value']['smartUrl']).strip()
			search_results.append(sr)
		return search_results