from django.shortcuts import render
from django.views.generic.edit import FormView
from sastakart.models import *
from django.http import HttpResponseRedirect,HttpResponse,StreamingHttpResponse,HttpRequest
import urllib2
from urllib2 import urlopen, Request
from bs4 import BeautifulSoup
from django.conf import settings
from django.views.generic import TemplateView
import json
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
import cloudinary
from cloudinary import uploader, api
from math import ceil
from django.http import Http404
from sastakart.api.amazon_reviews import *
from sastakart.api.flipkart_reviews import *
from sastakart.api.snapdeal_reviews import *



class SearchBarView(TemplateView):
	
	def post(self,request):
		if 'search_submit' in request.POST:
			
			if request.POST['search_text'] != '' and request.POST['search_text'] != None:
				keyword=request.POST['search_text'].strip().replace(' ','+')
				return HttpResponseRedirect(reverse('sastakart:search',kwargs={'keyword':keyword.lower(), 'page':1 }))
			else:
				raise Http404()
		else:
			raise Http404()


class SearchFormView(TemplateView):
	template_name = "index.html"

	
	def get_context_data(self, **kwargs):
		context = super(SearchFormView, self).get_context_data(**kwargs)
		top_scores = (Product.objects
				                     .order_by('-clicked')
				                     .values_list('clicked', flat=True).distinct()
				                     )
		top_records = (Product.objects
				                      .order_by('-clicked')
				                      .filter(clicked__in=top_scores[:5]))
		context['products'] = top_records[:5]
		rcat= Category.objects.filter(parent=None).order_by('name')
		context['root_categories'] = rcat

		return context


	

class SearchResultView(TemplateView):
	template_name='category-full.html'

	def get_context_data(self, **kwargs):
		context = super(SearchResultView, self).get_context_data(**kwargs)
		request = Request(settings.MSP_URL_KEYWORD % (kwargs['keyword'].lower(),str(kwargs['page']) ) )
		jso=urlopen(request).read()
		js = json.loads(jso)
		try:
			count = int(js['count'])
		except TypeError:
			count = 0
		count_pages = int(ceil(count/50.0))
		products=[]
		for item in js['items']:
			product={}
			product['title']=item['title']
			product['url']=settings.MSP_URL_PRODUCT % item['id']
			product['id']=item['id']
			product['price']=item['final_price']
			if Product.objects.filter(msp_id=product['id']).count() > 0:
				product['epid']=Product.objects.get(msp_id=product['id']).slug
			else:	
				product['epid']=msp_encode(product['id'])
			try:
				product['image']=item['image_list_grid']
			except KeyError:
				product['image']=item['image']
			products.append(product)
		context['products'] = products
		context['keyword']=kwargs['keyword']
		context['page']=page=int(kwargs['page'])
		context['count_p'] = count_pages
		context['count_num'] = count
		arr_num_p=[]
		# FOR 3 PAGES
		if page%3 == 1:
			for i in range(int(kwargs['page']),int(kwargs['page']) + 3):
				if i <= count_pages: 
					arr_num_p.append(i)
		elif page%3 == 2:
			for i in range(int(kwargs['page']) - 1,int(kwargs['page']) - 1 + 3):
				if i <= count_pages:
					arr_num_p.append(i)	
		else:
			for i in range(int(kwargs['page']) - 2,int(kwargs['page']) - 2 + 3):
				if i <= count_pages:
					arr_num_p.append(i)
					
		context['arr_num_p']=arr_num_p	
		return context
	


        
class ProductView(TemplateView):
	template_name='detail.html'


	def add_listing(self, js, store, product, category):
		try:
			if len(js['lines'][store]) >1:
				key= js['lines'][store]['listings'].keys()[0]
				listing= js['lines'][store]['listings'][key]
				request = Request(listing['store_url'])
				html=urlopen(request).read()
				soup=BeautifulSoup(html,'lxml')
				surl=soup.find('a',{'class':'store-link'})['href'].split('?')[0]
				if 'gp/offer-listing' in surl:
					surl = surl.replace('gp/offer-listing','dp')
				lis,created=Listing.objects.get_or_create(store=listing['store'], product=product, category= category)
				if created:
					lis.shipping_cost=get_json(listing,'shipping_cost')
					lis.mrp=get_json(listing,'mrp')
					lis.price=get_json(listing,'price')
					lis.delivery_days=get_json(listing,'delivery')
					lis.cod=bool(int(get_json(listing,'cod')))
					lis.offers=get_json(listing,'offers')
					lis.store_url=surl
					lis.category=category
					lis.save()
				return lis
			else:
				return None
		except KeyError:
			return None

	def get_context_data(self, **kwargs):
		context = super(ProductView, self).get_context_data(**kwargs)
		ppid=None
		try:
			ppid=Product.objects.get(slug=kwargs['epid'])
		except ObjectDoesNotExist:
			pass	
		
		try:
			if ppid is None:
				pid=msp_decode(kwargs['epid'])
			else:
				pid=ppid.msp_id	
		except Exception:
			raise Http404()		

		

		request = Request(settings.MSP_URL_PRODUCT % pid)
		try:
			jso=urlopen(request).read()
		except Exception:
			raise Http404()	
		js= json.loads(jso)
		subcategory, sub_created=Category.objects.get_or_create(name=js['subcategory'].lower()) 
		if sub_created:
			category,_= Category.objects.get_or_create(name=js['category'].lower(),parent=Category.objects.get(name=Category_Choices[pid.split(':')[0]] ))
			category.save()
			subcategory.parent=category
			subcategory.save()
		prod,created= Product.objects.get_or_create(msp_id=pid)
		if created:
			
			prod.clicked = 1
			prod.title= js['title']	
			prod.brand=js['brand']
			prod.category=subcategory	
			if get_json(js=js,param='reviews_info'):
				prod.rating =get_json( js=get_json(js=js,param='reviews_info'), param='avg_rating')
				prod.no_of_ratings= get_json( js=get_json(js=js,param='reviews_info'), param='ratings')
			prod.model=get_json(js=js,param='model')
			prod.save()
			img_url=None
			try:
				if len(js['images'][0]['single']) >0:
					img_url=js['images'][0]['single'][0]
				elif len(js['images'][0]['full_size']) >0:
					img_url=js['images'][0]['full_size'][0]
				else:
					img_url = js['images'][0]['thumb'][0]
			except KeyError:
				if len(js['images']['single']) >0:
					img_url=js['images']['single'][0]
				elif len(js['images']['full_size']) >0:
					img_url=js['images']['full_size'][0]
				else:
					img_url = js['images']['thumb'][0]
			p=cloudinary.uploader.upload(img_url)
			prod.image_url=p['url']
			prod.save()
		else:
			prod.clicked += 1
			prod.save()
			context['epid']	 = prod.slug
		listings=[]
		for store in settings.OUR_STORES:
			try:
				lis=self.add_listing(js=js,store=store, product=prod, category= subcategory.parent)
				if lis:
					listings.append(lis)
			except AttributeError:
				pass	

		try:
			for ls in listings:
				try:
					if len(Review.objects.filter(listing=ls)) == 0:
						if ls.store == 'amazon':
							rev_arr = amazon_reviews(ls.store_url.split('/')[4])	
							for rev in rev_arr:
								Review.objects.create(listing=ls,title=rev['title'],reviewer=rev['reviewer'],date=rev['date'],content=rev['content'])
						elif ls.store == 'flipkart':
							rev_arr2 = flip_rev(ls.store_url.replace('/p/','/product-reviews/'))		
							for rev in rev_arr2:
								Review.objects.create(listing=ls,title=rev['title'],reviewer=rev['reviewer'],date=rev['date'],content=rev['content'])
						elif ls.store == 'snapdeal':
							rev_arr3 = snap_rev(ls.store_url + '/reviews?page=1&sortBy=HELPFUL')	
							for rev in rev_arr3:
								Review.objects.create(listing=ls,title=rev['title'],reviewer=rev['reviewer'],date=rev['date'],content=rev['content'])				
				except Exception as e:
					print "tatti"
					pass					
		except Exception as e:
			print 'ttttt'
			pass		



		context['product']=prod
		try:
			init_p = listings[0].price
			lowest_ls ={}
			for ls in listings:
				if ls.price <= init_p:
					lowest_ls['price'] = ls.price
					lowest_ls['mrp'] = ls.mrp
					lowest_ls['url'] = ls.store_url
					lowest_ls['store'] = ls.store
					init_p = ls.price
			if lowest_ls is not None and lowest_ls['mrp']!=0.0:
				try:
					lowest_ls['discount'] = int(round((((lowest_ls['mrp'] - lowest_ls['price'])/lowest_ls['mrp']) * 100) , 0))
				except:
					pass	
					
			if lowest_ls['mrp'] == 0 or lowest_ls['mrp'] == 0.0 or lowest_ls['mrp'] == None or lowest_ls['mrp'] == 'None' or lowest_ls['mrp'] == '0':
				lowest_ls['mrp'] = None	
				
					
			lowest_ls['store'] = lowest_ls['store'].title()
			context['lowest'] = lowest_ls
		except IndexError:
			pass	

		for ls in listings:
			if ls.store == 'amazon':
				ama_rev_ls = Review.objects.filter(listing=ls)
				for x in ama_rev_ls:
					x.content = x.content.replace('<br/>','\n')

				context['ama_rev'] = ama_rev_ls
				context['ama_url'] = ls.store_url
				context['ama_price'] = ls.price
			elif ls.store == 'flipkart':
				flip_rev_ls = Review.objects.filter(listing=ls)
				for x in flip_rev_ls:
					x.content = x.content.replace('<br/>','\n')
				context['flip_rev'] = flip_rev_ls
				context['flip_url'] = ls.store_url
				context['flip_price'] = ls.price
			elif ls.store == 'snapdeal':
				snap_rev_ls = Review.objects.filter(listing=ls)
				for x in snap_rev_ls:
					x.content = x.content.replace('<br/>','\n')
				context['snap_rev'] = snap_rev_ls
				context['snap_url'] = ls.store_url
				context['snap_price'] = ls.price
			else:
				context['pay_url'] = ls.store_url	
				context['pay_price'] = ls.price	
			
		if len(listings) == 0:
			try:
				cloudinary.uploader.destroy(prod.image_url.split('/')[7].split('.')[0], invalidate = True)
			except IndexError:
				pass
			lis=Listing.objects.filter(product=prod)
			for li in lis:
				li.delete()
			prod.delete()
		if prod.image_url is None or prod.image_url =='':
			lis=Listing.objects.filter(product=prod)
			for li in lis:
				li.delete()
			try:
				cloudinary.uploader.destroy(prod.image_url.split('/')[7].split('.')[0], invalidate = True)
			except IndexError:
				pass
			prod.delete()

		top_scores = (Product.objects
				                     .order_by('-clicked')
				                     .values_list('clicked', flat=True).distinct()
				                     )
		top_records = (Product.objects
				                      .order_by('-clicked')
				                      .filter(clicked__in=top_scores[:5]))
		context['products'] = top_records[:5]

		return context

class FAQView(TemplateView):
	template_name = 'faq.html'

class ContactView(TemplateView):
	template_name = 'contact.html'

class AboutView(TemplateView):
	template_name = 'text.html'
