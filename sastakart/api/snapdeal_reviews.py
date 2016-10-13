from bs4 import BeautifulSoup
from urllib2 import Request, urlopen
import unicodedata


def snap_rev(url):
	request = Request(url)
	request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117')
	html = urlopen(request,timeout=20).read()
	soup = BeautifulSoup(html,'lxml')
	arr = []
	try:
		rev_list = soup.find_all('div',{'class':'commentlist first'})
		
		for x in range(5):
			try:
				lst = {}
				lst['reviewer'] = rev_list[x].find('span',{'class':'_reviewUserName'}).text.strip()
				t1 = rev_list[x].find('div',{'class':'user-review'})
				lst['date'] = t1.find('div',{'class':'date LTgray'}).text.strip()
				lst['title'] = t1.find('div',{'class':'head'}).text.strip()
				htmlContent = ''
				for s in t1.p.contents:
					if '\n' in s:
						s=s.replace('\n','<br/>')
					try:
						htmlContent += unicodedata.normalize('NFKD', s).encode('ascii','ignore')
					except TypeError:
						htmlContent += str(s)
				# htmlContent.replace('\n','<br/>')		
				lst['content'] = htmlContent
				arr.append(lst)
			except:
				pass	
	except:
		pass	
	return arr	

# print snap_rev('http://www.snapdeal.com/product/infocus-m810-16-gb-gold/671993423251/reviews?page=1&sortBy=HELPFUL')[0]['content']	