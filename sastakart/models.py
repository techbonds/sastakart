from django.db import models
import datetime
from django.utils import timezone
from mptt.models import TreeForeignKey, MPTTModel
from sastakart.models import *
from autoslug import AutoSlugField

Category_Choices={
	'e':'Electronics',
	'f':'Fashion',
	}
def msp_encode(pid):
	return pid.split(':')[0] + '-' + str(int(pid.split(':')[1])*3)

def msp_decode(epid):
	return epid.split('-')[0] + ':' +  str(int(epid.split('-')[1])/3)

def get_json(js,param):
	try:
		return js[param]
	except KeyError:
		return None

class Category(MPTTModel):
	name = models.CharField(max_length=200,unique=True)
	parent = TreeForeignKey('self', null=True, blank=True, related_name='children', default=None)

	def __unicode__(self):
		return self.name

	class MPTTMeta:
		order_insertion_by = ['name']

class Product(models.Model):
	title= models.CharField(max_length=200,null=True, blank=True, default='SKP')
	rating=models.FloatField(null=True,default=0.0,blank=True)
	no_of_ratings=models.IntegerField(null=True,default=0,blank=True)
	model=models.CharField(max_length=400,null=True,blank=True)
	brand=models.CharField(max_length=200,null=True,blank=True)
	image_url=models.CharField(max_length=200,null=True,blank=True)
	msp_id=models.CharField(max_length=100,null=True,blank=True)
	category= models.ForeignKey('Category',null=True,blank=True)
	slug = AutoSlugField(populate_from='title', always_update=True, unique=True)
	date_created=models.DateTimeField(default=timezone.now)
	clicked = models.IntegerField(null=True,blank=True,default=0)

	def __unicode__(self):
		return str(self.id)+': ' +self.title

class Listing(models.Model):
	store=models.CharField(max_length=200,null=True,blank=True)
	store_url=models.CharField(max_length=200,null=True,blank=True)
	shipping_cost=models.FloatField(null=True,blank=True,default=0.0)
	mrp=models.FloatField(null=True,blank=True,default=0.0)
	price=models.FloatField(null=True,blank=True,default=0.0)
	delivery_days=models.CharField(max_length=200,null=True,blank=True)
	cod=models.BooleanField(blank=True,default=False)
	offers=models.CharField(max_length=1000,null=True,blank=True)
	product=models.ForeignKey(Product, on_delete=models.PROTECT,null=True,blank=True)
	last_updated=models.DateTimeField(default=timezone.now)
	
	def __unicode__(self):
		return str(self.id) + ': ' + self.store

class Review(models.Model):
	listing = models.ForeignKey(Listing, null=True, blank=True)
	title = models.CharField(max_length=200, null=True, blank=True)
	reviewer = models.CharField(max_length=200, null=True, blank=True)
	date = models.CharField(max_length=200, null=True, blank=True)
	content = models.TextField(null=True, blank=True)


	def __unicode__(self):
		return str(self.id) + ': ' + self.reviewer 
