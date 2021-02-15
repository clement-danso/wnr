"""
Custom management command that sends an email to all users
born on the current day and month.
"""
import requests
import json
from datetime import date

from django.core.management import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
#from someplace import User
from smsapp.models import records, delivery


class Command(BaseCommand):
	def handle(self, **options):
		today = timezone.now().date()
		for record in records.objects.filter(FirstAppDate__day=today.day, FirstAppDate__month=today.month):
			
			age= date.today()-record.FirstAppDate
			age_in_days=age.days
			age_in_yrs = age_in_days/365
		
			#subject = 'Happy birthday %s!' % records.FirstName
			#body = 'Hi %s,\n...' + user.first_name
			#send_mail(subject, body, 'contact@yourdomain.com', [user.email])
			
			endPoint = 'https://api.mnotify.com/api/sms/quick'
			apiKey = 'rT5L5lrhhoCaP0BfKlSU9dNh6Vqp5RFwLKhQ6I8n7KyWL'
			data = {
			   'recipient[]': [record.Mobile],
			   'sender': 'HR WNRHD',
			   'message': "Hello {}, congratulations on your {} th service anniversary today! You have been such significant part of our team and we couldn't imagine our workplace without you. Happy work anniversary!" .format(record.FirstName, age_in_yrs),
			    
			   'is_schedule': False,
			   'schedule_date': ''
			}
			url = endPoint + '?key=' + apiKey
			response = requests.post(url, data)
			data = response.json()
			
			print(data)
