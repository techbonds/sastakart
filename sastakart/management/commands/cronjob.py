from django.core.management.base import BaseCommand, CommandError
from sastakart.models import *
import schedule
from sastakart.api import amazon, flipkart, snapdeal , paytm
import time
from django.utils import timezone
import smtplib
import os
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

class Command(BaseCommand):
	help = 'Updates the listings daily.'

	def handle(self, *args, **options):
		lisitngs= Listing.objects.all().order_by('id')
		try:
			os.remove('cron_logs.txt')
		except OSError:
			pass
		log_file= open('cron_logs.txt','w')
		a=amazon.amazon()
		f=flipkart.flipkart()
		s=snapdeal.snapdeal()
		p=paytm.paytm()
		count=0
		self.stdout.write('CRON JOB STARTED!!')
		for listing in lisitngs:
			self.stdout.write(str(listing.id)+ listing.store)
			if listing.store == 'amazon':
				try:
					listing.price = float(a.offer_listing(listing.store_url)[0]['price'])
					listing.last_updated = timezone.now()
					log_file.write(str(listing.id)+' , '+str(listing.store)+'\n')
					listing.save()
					count+=1
				except Exception as e:
					log_file.write(str(listing.id)+' , '+str(listing.store)+' '+str(e)+'\n')
					self.stdout.write('Exception:'+ str(e))
			elif listing.store == 'flipkart':
				try:
					listing.price = float(f.product_details(listing.store_url)['offers'][0]['price'])
					listing.last_updated = timezone.now()
					log_file.write(str(listing.id)+' , '+str(listing.store)+'\n')
					listing.save()
					count+=1
				except Exception as e:
					log_file.write(str(listing.id)+' , '+str(listing.store)+' '+str(e)+'\n')
			elif listing.store == 'snapdeal':
				try:
					listing.price = float(s.offer_listing(listing.store_url)[0]['price'])
					listing.last_updated = timezone.now()
					log_file.write(str(listing.id)+' , '+str(listing.store)+'\n')
					listing.save()
					count+=1
				except Exception as e:
					log_file.write(str(listing.id)+' , '+str(listing.store)+' '+str(e)+'\n')
			if listing.store == 'paytm':
				try:
					listing.price = float(p.product_details_api(listing.store_url)['price'])
					listing.last_updated = timezone.now()
					log_file.write(str(listing.id)+' , '+str(listing.store)+'\n')
					listing.save()
					count+=1
				except Exception as e:
					log_file.write(str(listing.id)+' , '+str(listing.store)+' '+str(e)+'\n')

		log_file.write(str(count)+' LISTINGS SUCCESSFULLY UPDATED!\n')
		log_file.close()
		self.stdout.write(str(count)+' LISTINGS SUCCESSFULLY UPDATED!')
		self.send_mail(
		send_from = '',
		send_to = [''],
		subject = 'CronJob Logs',
		text = str(count)+' LISTINGS SUCCESSFULLY UPDATED!\nPlease find the attached logs.',
		login = '',
		password = '',
		attach = 'cron_logs.txt')
		self.stdout.write('MAIL SENT!!')




	def send_mail(self,send_from, send_to, subject, text,login, password, attach):
		assert isinstance(send_to, list)
		server='smtp.mail.yahoo.com'
		msg = MIMEMultipart()
		msg['Subject']=subject
		msg['To']=COMMASPACE.join(send_to)
		msg['Date']=formatdate(localtime=True)
		msg.attach(MIMEText(text))

		server = smtplib.SMTP_SSL(server,465)
		server.login(login,password)
		server.sendmail(send_from, send_to, msg.as_string())
		server.close()