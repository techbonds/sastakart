from urllib2 import urlopen , Request
from bs4 import BeautifulSoup
import pprint
# import tablib
import json
from sys import argv
from urlparse import urlparse
base_url="http://www.amazon.in/s/ref=nb_sb_noss?url=search-alias=aps&field-keywords="
class amazon:
	max_attempts=0
	def __init__(self):
		pass

	def product_details(self,url):
		# print "AMAZON...product_details"
		product={}
		html=urlopen(url,timeout=10).read()
		soup=BeautifulSoup(html,"lxml")

		r1= soup.find(id="price")
		r2= r1.table.find_all("tr")
		mrp= r2[0].find_all("td")[1].text.strip()
		mrp=''.join(mrp.split(','))
		bb_price = r2[1].find_all("td")[1].span.text.strip()
		bb_price = ''.join(bb_price.split(','))
		r3= soup.find(id="averageCustomerReviews")
		if(r3.find(id="acrPopover")):
			rating= r3.find(id="acrPopover")['title'].strip()[0]

		else:
			rating="0"
		if(r3.find(id="acrCustomerReviewText")):
			reviews= r3.find(id="acrCustomerReviewText").text.strip()[:-17]
		elif(r3.find(id="acrCustomerWriteReviewText")):
			reviews="0"
		else:
			reviews="not available"
		if(soup.find(id="altImages")):
			images=len(soup.find(id="altImages").find_all("li",{"class":"a-spacing-small item"}))
		else:
			images=0
		if(soup.find(id="a-page")):
			description=soup.find(id="a-page")#.find("div",{"class":"a-container"}).find(id="iframe-wrapper")#.find("div",{"class":"productDescriptionWrapper"}).text.strip()
		else:
			description=None
		product['mrp']=mrp
		product['price']=bb_price
		product['reviews']=reviews
		product['images']=images
		product['rating']=rating
		product['description']=description
		# print"MRP: "+ product['mrp']
		# print "BB Price: " + product['price']
		# print "Rating: "+ product['rating']
		# print "No. of Reviews: "+ product['reviews']
		# print "No. of Images: "+str(product['images'])
		
		# print product['description'].encode(encoding='UTF-8',errors='strict')	
		# print "....Done"
		return product	

	def search(self,keyword,page=1):
		num_of_results=page*16
		search_results=[]
		html=urlopen(base_url+keyword+"&page="+str(page),timeout=10).read()
		soup=BeautifulSoup(html,"lxml")
		for x in range(0,num_of_results):
			s_res={}
			res_obj=soup.find(id="result_"+str(x))
			try:
				r1=res_obj.find("div",{"class":"a-fixed-left-grid-col a-col-right"})
				if(r1):
					name=r1.find("div").a.h2.text.strip()
					link=str(r1.find("div").a['href'].strip())
					ref_link=urlparse(link).path.split('/')[3]
					s_res['name'] = name
					s_res['url']=link
					s_res['reference_code']=ref_link
					search_results.append(s_res)
			except AttributeError:
				print "Product not found"
				break
		return search_results
				

	def get_seller_name(self,link):
		while(True):	
			try:
				html=urlopen(link,timeout=10).read()
				soup=BeautifulSoup(html,"lxml")
				r1=soup.find("div",{"id":"s-result-info-bar-content"})
				name=r1.div.div.h2.span.span.text.strip()
				return name
			except Exception,e:
				print "get_seller_name "+str(e)
				pass
			else:
				break

	def offer_listing(self,url):
		ref_link=urlparse(url).path.split('/')[2]
		# print ref_link
		ol_url='http://www.amazon.in/gp/offer-listing/'
		offers=[]
		soup=None
		# print "AMAZON...offer_listing"

		html=urlopen(ol_url+ref_link,timeout=10).read()
		soup=BeautifulSoup(html,"lxml")


		r1=soup.find_all("div",{"class":"a-row a-spacing-mini olpOffer"})
		for x in range(0,len(r1)):
			r2=r1[x].find("div",{"class":"a-column a-span2"})
			price=r2.span.span.text.strip()
			price=''.join(price.split(','))
			r3=r1[x].find("div",{"class":"a-column a-span2 olpSellerColumn"})
#UNCOMMENT FOR SELLER NAME
			# if(not r3.a.text):
			# 	seller_link=r3.a['href']
			# 	seller_name=self.get_seller_name(seller_link)
			# 	seller_name= seller_name.strip()[:-11]
			# else:
				# seller_name= r3.a.text
			# print price,seller_name
			offer={}
			# offer['seller']=seller_name
			offer['price']=price[4:]
			offers.append(offer)
			# print price+"  BY  "+ offer['seller']
		self.max_attempts=0
		# print "....Done"
		return offers

	
	def search_api(self,keyword):
		search_results=[]
		keyword = keyword.replace(' ','+')
		request = Request('https://www.amazon.in/s/ref=nb_sb_noss?k=%s&dataVersion=v0.2&cid=08e6b9c8bdfc91895ce634a035f3d00febd36433&format=json' % keyword)
		html=urlopen(request).read()
		html_json=json.loads(html)
		# print html_json
		for product in html_json['results']['sections'][0]['items']:
			sr={}
			sr['name'] = product['title']
			sr['url'] = 'http://www.amazon.in/dp/' + product['asin']
			search_results.append(sr)
		return search_results	

	

# a= amazon()
# z=a.search('dell')
# pp = pprint.PrettyPrinter(indent=20)
# pp.pprint(z)
# print(a.product_details('http://www.amazon.in/Dell-MS111-Optical-Mouse-Black/dp/B009W2U5BQ/'))

# a.offer_listing('http://www.amazon.in/Dell-MS111-Optical-Mouse-Black/dp/B009W2U5BQ/')
# print a.search_api('dell inspiron')