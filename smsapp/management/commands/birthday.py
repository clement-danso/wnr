"""
Custom management command that sends an email to all users
born on the current day and month.
"""
import requests
import json

from django.core.management import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
#from someplace import User
from smsapp.models import records, delivery


class Command(BaseCommand):
	def handle(self, **options):
		today = timezone.now().date()
		for record in records.objects.filter(DOB__day=today.day, DOB__month=today.month):
			#subject = 'Happy birthday %s!' % records.FirstName
			#body = 'Hi %s,\n...' + user.first_name
			#send_mail(subject, body, 'contact@yourdomain.com', [user.email])
			
			endPoint = 'https://api.mnotify.com/api/sms/quick'
			apiKey = 'rT5L5lrhhoCaP0BfKlSU9dNh6Vqp5RFwLKhQ6I8n7KyWL' 
			data = {
			   'recipient[]': [record.Mobile],
			   'sender': 'HR WNRHD',
			   'message': 'Dear %s, the Western North Regional Health Directorate wishes you a happy birthday, a wonderful year and success in all you do.' % record.FirstName,
			   'is_schedule': False,
			   'schedule_date': ''
			}
			url = endPoint + '?key=' + apiKey
			response = requests.post(url, data)
			data = response.json()
			
			bstatus=json.dumps(data['status'])
			bsmstype='Birthday'
			btotalsent=json.dumps(data["summary"]["total_sent"])
			btotalrejected=json.dumps(data["summary"]["total_rejected"])
			brecipient=json.dumps(data["summary"]["numbers_sent"])
			bcreditused=json.dumps(data["summary"]["credit_used"])
			bcreditleft=json.dumps(data["summary"]["credit_left"])
			
			delivery_instance = delivery(
										sms_status=bstatus, 
										smstype=bsmstype, 
										total_sent=btotalsent, 
										total_rejected=btotalrejected, 
										recipient=brecipient, 
										credit_used=bcreditused, 
										credit_left=bcreditleft
										)
			delivery_instance.save()
