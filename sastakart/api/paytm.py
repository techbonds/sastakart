from urllib2 import urlopen,Request
from bs4 import BeautifulSoup
import pprint
# import tablib
import json
import time
from urlparse import urlparse
import math

class paytm:

	def product_details_api(self,url):
		netloc= 'catalog.'+urlparse(url).netloc
		path= '/v1/'+urlparse(url).path.split('/',2)[2]
		api_url= urlparse(url).scheme + '://'+netloc+path
		request = Request(api_url)
		html=urlopen(request).read()
		result=json.loads(html)
		product={}
		product['mrp']=result['actual_price']
		price=float(result['offer_price'])
		discount= result['tag'][:-4]
		# print discount[1:]

		if discount[-1:] == '%':
			product['price']=math.ceil( price - (price*(float(discount[1:-1])/100)) )
			# print product['price'] 
		elif discount[:1]=='+':
			product['price']= price - int(discount[1:])


		return product



# p= paytm()
# p.product_details_api('https://paytm.com/shop/p/hp-15-r249tu-notebook-l2z88pa-ci3-4th-gen-4-gb-ram-1-tb-hdd-15-6-inch-free-dos-black-LAPHP-15-R249TUSARA73397CDD2F9F3')