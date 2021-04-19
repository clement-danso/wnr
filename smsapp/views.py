from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from smsapp.models import *
from smsapp.forms import *
import requests
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
#

def record_create(request):
    form = RecordsForm()
    context = {'form': form}
    html_form = render_to_string('smsapp/partial_record_create.html',
        context,
        request=request,
    )
    return JsonResponse({'html_form': html_form})


@login_required
def load_grades(request):
    category_id = request.GET.get('category_id')
    grades = grade.objects.filter(category_id=category_id).order_by('grade')
    
    return render(request, 'smsapp/grades_dropdown_list_options.html', {'grades': grades})

@login_required
def validate_empnumber(request):
    EmpNumber = request.GET.get('EmpNumber')
    data = {
        'is_taken': records.objects.filter(EmpNumber__iexact=EmpNumber).exists()
    }
    print(data)
    return JsonResponse(data)


def records_update(request):
    EmpNumber = request.GET.get('EmpNumber')
    recod = records.objects.filter(Empnumber__iexact=Empnumber)
    
    return JsonResponse(recod)


@login_required
def home(request):
	today = timezone.now().date()
	alrecods=records.objects.all()
	recods=records.objects.all().order_by('-date_created')[:5]
	deliveries=delivery.objects.all().order_by('-date_created')[:5]
	aldeliveries=delivery.objects.all()
	act_recods=records.objects.filter(status='Active')
	inact_recods=records.objects.filter(status='Inactive')
	
	bdaysms=delivery.objects.filter(smstype='Birthday').count()
	annisms=delivery.objects.filter(smstype='Anniversary').count()
	bsms=delivery.objects.filter(smstype='Broadcast').count()
	welsms=delivery.objects.filter(smstype='Welcome').count()
	
	recodsnum=alrecods.count()
	activenum=act_recods.count()
	inactivenum=inact_recods.count()
	
	context={
		'recods':recods,
		'recodsnum':recodsnum,
		'activenum':activenum, 
		'inactivenum':inactivenum, 
		'deliveries':deliveries,
		'aldeliveries':aldeliveries,
		'alrecods':alrecods,
		'bdaysms': bdaysms,
		'annisms': annisms,
		'bsms': bsms,
		'welsms': welsms,
		} 
	return render(request, 'smsapp/dashboard.html', context)


@login_required
def createrecord(request):
	"""form page for creating records"""

	fm = RecordsForm()
	if request.method == 'POST':
		fm = RecordsForm(request.POST)
		
		if fm.is_valid():
			fm.save()
			

			fon=request.POST.get('Mobile')
			titlename=request.POST.get('Title')
			firstname=request.POST.get('FirstName')
			lastname=request.POST.get('LastName')
			emaill=request.POST.get('OfficialEmail')
			dateOB=request.POST.get('DOB')
			
			
			endPoint = 'https://api.mnotify.com/api/sms/quick'
			apiKey = 'rT5L5lrhhoCaP0BfKlSU9dNh6Vqp5RFwLKhQ6I8n7KyWL'
			data = {
				'recipient[]': fon,
				'sender': 'HR WNRHD',
				'message': 'Dear %s, You are welcome to the Western North Regional Health Directorate SMS platform. Thank you for joining this great health family.\nNB: This is a test \n\nRSVP: 0204912857' % firstname,
				'is_schedule': False,
				'schedule_date': ''
				}
			url = endPoint + '?key=' + apiKey
			response = requests.post(url, data)
			data = response.json()
			
			bstatus=json.dumps(data['status'])
			bsmstype='Welcome'
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
		return redirect('/home')
		
	context = {'fm':fm}
	
	return render(request, 'smsapp/recordfrm.html', context)

def updaterecord(request, pk):
	"""form page for creating orders"""
	record = records.objects.get(EmpNumber=pk)
	fm = RecordsForm(instance=record)
	
	if request.method == 'POST':
		fm = RecordsForm(request.POST or None, instance=record)
		if fm.is_valid():
			fm.save()
			return redirect('/recordlist')
	else:
		fm = RecordsForm(instance=record)
	
	context = {'fm':fm}
	return render (request, 'smsapp/recordfrm.html', context)


@login_required
def creategroup(request):
	
	fm = GroupForm()
	if request.method == 'POST':
		fm = GroupForm(request.POST)
		
		if fm.is_valid():
			fm.save()
		
		
		return redirect('/grouplist')

	context = {'fm':fm}
	return render(request, 'smsapp/groupfrm.html', context)


@login_required
def bcriteria(request):
	crit=request.POST.get('criteria')
	if request.method == 'POST' and crit=='district':
		return redirect('/newbmessagedis')
	elif request.method =='POST' and crit=='category':
		return redirect('/newbmessagecat')
	
	
	
		
	context = {}
	return render(request, 'smsapp/bcriteria.html', context)

@login_required
def createbmessagedis(request):
	"""form page for creating records"""
	fm = BroadcastmessagedisForm()
	if request.method == 'POST':
		fm = BroadcastmessagedisForm(request.POST)
		dist=request.POST.get('district')
		
		dist_records=records.objects.filter(bmc__subdistrict__district=dist)
		
		cont=request.POST.get('Content')
		
		for recod in dist_records:
			endPoint = 'https://api.mnotify.com/api/sms/quick'
			apiKey = 'rT5L5lrhhoCaP0BfKlSU9dNh6Vqp5RFwLKhQ6I8n7KyWL'
			data = {
			   'recipient[]': [recod.Mobile],
			   'sender': 'HR WNRHD',
			   'message': cont,
			   'is_schedule': False,
			   'schedule_date': ''
			}
			url = endPoint + '?key=' + apiKey
			response = requests.post(url, data)
			data = response.json()
			
			bstatus=json.dumps(data['status'])
			bsmstype='Broadcast'
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
			
			return redirect('/home')
	
	context = {'fm':fm}
	
	return render(request, 'smsapp/bcmessagedisfrm.html', context)

@login_required
def createbmessagecat(request):
	"""form page for creating records"""
	fm = BroadcastmessagecatForm()
	if request.method == 'POST':
		fm = BroadcastmessagecatForm(request.POST)
		cat=request.POST.get('category')
		
		cat_records=records.objects.filter(category=cat)
		
		cont=request.POST.get('Content')
		
		for recod in group_records:
			endPoint = 'https://api.mnotify.com/api/sms/quick'
			apiKey = 'rT5L5lrhhoCaP0BfKlSU9dNh6Vqp5RFwLKhQ6I8n7KyWL'
			data = {
			   'recipient[]': [recod.Mobile],
			   'sender': 'HR WNRHD',
			   'message': cont,
			   'is_schedule': False,
			   'schedule_date': ''
			}
			url = endPoint + '?key=' + apiKey
			response = requests.post(url, data)
			data = response.json()
			
			bstatus=json.dumps(data['status'])
			bsmstype='Broadcast'
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
			
			return redirect('/home')
	
	context = {'fm':fm}
	
	return render(request, 'smsapp/bcmessagecatfrm.html', context)

@login_required
def messtemp(request):
	fm=MesstempForm()
	if request.method == 'POST':
		fm = MesstempForm(request.POST)
		
		
		tit=request.POST.get('Title')
		cont=request.POST.get('Content')
		
		endPoint = 'https://api.mnotify.com/api/template'
		apiKey = 'rT5L5lrhhoCaP0BfKlSU9dNh6Vqp5RFwLKhQ6I8n7KyWL'
		data = {
		   'title': tit,
		   'content': cont
		}
		url = endPoint + '?key=' + apiKey
		response = requests.post(url, data)
		data = response.json()
		
		messtemp_id=json.dumps(data["_id"])
		messtemp_instance = messagetemp(Template_id=messtemp_id, Title=tit, Content=cont)
		messtemp_instance.save()
		
		return redirect('/home')
	
	context = {'fm':fm}

	return render(request, 'smsapp/messtempfrm.html', context)

@login_required
def recordlist(request):
	recods=records.objects.all()

	
	context={'recods':recods}
	return render(request, 'smsapp/records.html', context)

@login_required
def grouplist(request):
	grps=group.objects.all()
	
	context={'grps':grps}
	return render(request, 'smsapp/groups.html', context)

@login_required	
def templatelist(request):
	temps=messagetemp.objects.all()
	
	context={'temps':temps}
	return render(request, 'smsapp/templates.html', context)


@login_required
def deliverylist(request):
	delivs=delivery.objects.all()
	
	context={'delivs':delivs}
	return render(request, 'smsapp/deliveries.html', context)

@login_required
def trying(request):
	recods=records.objects.all()
	#record = records.objects.get(EmpNumber=pk)
	fm = RecordsForm()
	
	context={'recods':recods, 'fm':fm}
	return render(request, 'smsapp/students_rv.ejs', context)	
	
