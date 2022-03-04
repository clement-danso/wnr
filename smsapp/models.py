from django.db import models

# Create your models here.
class region(models.Model):
	regionName = models.CharField(max_length = 100)
	
	def __str__(self):
		return self.regionName
	
class district(models.Model):
	districtName = models.CharField(max_length= 100)
	region = models.ForeignKey(region, null=True, on_delete=models.SET_NULL)
	
	def __str__(self):
		return self.districtName
	
class subdistrict(models.Model):
	subdistrictName = models.CharField(max_length=100)
	district = models.ForeignKey(district, null=True, on_delete=models.SET_NULL)
	
	def __str__(self):
		return self.subdistrictName
	
class bmc(models.Model):
	bmcName = models.CharField(max_length=100)
	subdistrict = models.ForeignKey(subdistrict, null=True, on_delete=models.SET_NULL)
	
	class Meta:
		ordering = ('bmcName',)
	
	def __str__(self):
		return self.bmcName
		

	
class group(models.Model):
	
	groupName = models.CharField(max_length=100)
	
	def __str__(self):
		return self.groupName


	
class unit(models.Model):
	unit = models.CharField(max_length=100)
	
	def __str__(self):
		return self.unit


class category(models.Model):
	catName = models.CharField(max_length=100)
	
	class Meta:
		verbose_name_plural='Categories'
		
	def __str__(self):
		return self.catName
		
class grade(models.Model):
	grade = models.CharField(max_length=100)
	category = models.ForeignKey(category, null=True, on_delete=models.SET_NULL)
	
	class Meta:
		ordering = ('grade',)
	
	def __str__(self):
		return self.grade 

class records(models.Model):
	GENDER = (
			 ('Male', 'Male'),
			 ('Female', 'Female'),
			
			 )
	TITLE = (
			 ('Mr.', 'Mr.'),
			 ('Mrs.', 'Mrs.'),
			 ('Miss.', 'Miss.'),
			 ('Dr.', 'Dr.'),
			
			 )
			 		 
	MARITAL_STATUS = (
			 ('Single', 'Single'),
			 ('Married', 'Married'),
			 ('Divorced', 'Divorced'),
			 ('Widowed', 'Widowed'),
			
			 )
			 
	RELIGION = (
			 ('Christian', 'Christian'),
			 ('Muslim', 'Muslim'),
			 ('Other', 'Other'),
			
			 )
			 
	STATUS = (
			 ('Active', 'Active'),
			 ('Inactive', 'Inactive'),
			
			 )
	
	EmpNumber = models.CharField(max_length=15,primary_key=True, verbose_name='Employment Number')
	Title = models.CharField(max_length=11, choices=TITLE, default=TITLE[0][0],null=True, blank=True)
	FirstName = models.CharField(max_length=50, verbose_name='First Name')
	LastName = models.CharField(max_length=50, verbose_name='Last Name')
	OtherName = models.CharField(max_length=50, verbose_name='Other Name', null=True, blank=True)
	Gender = models.CharField(max_length=10, choices=GENDER)
	DOB = models.DateField(verbose_name='Date of Birth')
	MaritalStatus = models.CharField(max_length=10, choices=MARITAL_STATUS, verbose_name='Marital Status', null=True, blank=True)
	Religion = models.CharField(max_length=10, choices=RELIGION, blank=True)
	OfficialEmail= models.CharField(max_length=50,verbose_name='Official Email', unique=True, null=True, blank=True)
	PersonalEmail= models.CharField(max_length=50, verbose_name='Personal Email',null=True, blank=True)
	Mobile = models.CharField(max_length=10, verbose_name='1st Mobile', unique=True)
	Mobile1 = models.CharField(max_length=10,verbose_name='2nd Mobile', null=True, blank=True)
	FirstAppDate = models.DateField(verbose_name='First Appointment Date')
	AssumptionDutyDate= models.DateField(verbose_name='Date of Assumption of Duty')
	category = models.ForeignKey(category, null=True, verbose_name='Category', on_delete=models.SET_NULL)
	grade = models.ForeignKey(grade, null=True, on_delete=models.SET_NULL)
	bmc = models.ForeignKey(bmc, null=True, verbose_name='BMC', on_delete=models.SET_NULL)
	unit = models.ForeignKey(unit, null=True, on_delete=models.SET_NULL, blank=True)
	status = models.CharField(max_length=10, choices=STATUS, default=STATUS[0][0], null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	date_updated = models.DateTimeField(auto_now=True, null=True)
	
	class Meta:
		verbose_name_plural = 'records'
	
	def __str__(self):
		return self.FirstName




class broadcastmessagedis(models.Model):
	
	
	Subject=models.CharField(max_length=50)
	Content=models.CharField(max_length=400)
	district=models.ForeignKey(district, null=True, on_delete=models.SET_NULL)
	
	
	class Meta:
		verbose_name_plural='District-based Broadcast Messages'
	
	def __str__(self):
		return self.Subject


class broadcastmessagecat(models.Model):
	
	
	Subject=models.CharField(max_length=50)
	Content=models.CharField(max_length=400)
	category=models.ManyToManyField(category)
	
	
	class Meta:
		verbose_name_plural='Category-based Broadcast Messages'
	
	def __str__(self):
		return self.Subject

class broadcastmessageall(models.Model):
	Subject=models.CharField(max_length=50)
	Content=models.CharField(max_length=400)
	
	class Meta:
		verbose_name_plural='Broadcast Messages to all'
	
	def __str__(self):
		return self.Subject

class delivery(models.Model):
	sms_status = models.CharField(max_length=50)
	smstype = models.CharField(max_length=50)
	total_sent = models.CharField(max_length=50)
	total_rejected = models.CharField(max_length=50)
	recipient=models.CharField(max_length=50)
	credit_used = models.CharField(max_length=50)
	credit_left = models.CharField(max_length=50)
	date_created = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		verbose_name_plural = 'Deliveries'
	
	def __str__(self):
		return self.sms_status

	


