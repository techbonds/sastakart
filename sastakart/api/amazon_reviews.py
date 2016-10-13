from urllib2 import urlopen , Request
from bs4 import BeautifulSoup
import unicodedata


def amazon_reviews(asin):
	url = 'http://www.amazon.in/product-reviews/%s/' % asin

	html=urlopen(url,timeout=20).read()
	soup=BeautifulSoup(html,"lxml")

	reviews = []
	try:
		raw = soup.find(id="cm_cr-review_list")
		lst = raw.find_all("div",{"class":"a-section review"})
		
		for i in range(0,5):
			try:
				
				rview = {}
				rview['title'] = lst[i].find_all('div')[1].find('a',{'class':'review-title'}).text
				rview['reviewer'] = lst[i].find_all('div')[2].span.a.text
				rview['date'] = lst[i].find_all('div')[2].find('span',{'class':'review-date'}).text.replace('on ','')
				htmlContent = ''
				for s in lst[i].find('span',{'class':'a-size-base review-text'}).contents:
					try:
						htmlContent += unicodedata.normalize('NFKD', s).encode('ascii','ignore')
					except TypeError:
						htmlContent += str(s)
				rview['content'] = htmlContent
				reviews.append(rview)

			except:
				pass	

	except:
		pass	
	return reviews