from bs4 import BeautifulSoup
from urllib2 import Request, urlopen
import unicodedata


def flip_rev(url):
	html = urlopen(url,timeout=20).read()
	soup = BeautifulSoup(html,'lxml')
	arr = []
	try:
		r = soup.find_all('div',{'class':'fclear fk-review fk-position-relative line '})
		
		for x in range(5):
			try:
				lst = {}
				try:
					lst['reviewer'] = r[x].find('a',{'class':'load-user-widget fk-underline'}).text.strip()
				except AttributeError:
					lst['reviewer'] = r[x].find('span',{'class':'fk-color-title fk-font-11 review-username'}).text.strip()
				lst['date'] = r[x].find('div',{'class':'date line fk-font-small'}).text.strip()
				lst['title'] = r[x].find('div',{'class':'line fk-font-normal bmargin5 dark-gray'}).strong.text.strip()
				# lst['content'] = r[x].find('span',{'class':'review-text'}).contents
				htmlContent = ''
				for s in r[x].find('span',{'class':'review-text'}).contents:
					try:
						htmlContent += unicodedata.normalize('NFKD', s).encode('ascii','ignore')
					except TypeError:
						htmlContent += str(s)
				lst['content'] = htmlContent		
				arr.append(lst)
			except:
				pass	
	except:
		pass		
	return arr		
# print flip_rev('http://www.flipkart.com/asus-zenfone-selfie/product-reviews/itmebpvek8z5yjyd')[1]['content']