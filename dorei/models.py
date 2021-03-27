from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse # Used to generate URLs by reversing the URL patterns

class Location(models.Model):
    location_id = models.IntegerField(db_column='location_id', primary_key=True)
    floor = models.IntegerField(db_column='floor',default=1)
    room = models.CharField(db_column='room', max_length=5, default=1)               #can change to IntegerField
    shelf = models.IntegerField(db_column='shelf',default=1)

    def __str__(self):
        return str(self.location_id)

class Book(models.Model):
    isbn = models.CharField(db_column='isbn', primary_key=True, max_length=13)
    author = models.CharField(db_column='author', max_length=256, null=True)
    subject = models.CharField(db_column='subject', max_length=50, blank=True)
    title = models.CharField(db_column='title', max_length=256)
    edition = models.IntegerField(db_column='edition', blank=True, null=True)
    location_id = models.ForeignKey(Location, on_delete = models.DO_NOTHING, null=True, blank=True, db_column='location_id')
    grade = models.IntegerField(db_column='grade', blank=True,null=True,validators=[MinValueValidator(1), MaxValueValidator(12)])

    def __str__(self):
        return self.isbn

class User(models.Model):
    user_id = models.AutoField(db_column='user_id', primary_key=True)
    first_name = models.TextField(db_column='first_name', max_length=10)
    middle_name = models.TextField(db_column='middle_name', max_length=10, blank=True, null=True)
    last_name = models.TextField(db_column='last_name', max_length=10, blank=True, null=True)
    email_address = models.EmailField(db_column='email_address', max_length=40)  
    house_number = models.CharField(db_column='house_number', max_length=10, blank=True, null=True) 
    street_number = models.CharField(db_column='street_number', max_length=10, blank=True, null=True)  
    street_name = models.TextField(db_column='street_name', max_length=50)   
    city = models.TextField(db_column='city', max_length=50)  
    state = models.TextField(db_column='state', max_length=50)  
    postal_code = models.DecimalField(db_column='postal_code', max_digits=6, decimal_places=0) 
    password = models.CharField(db_column='password', max_length=256) 

    def __str__(self):
        """String for representing the Model object."""
        return self.email_address

class BookDonate(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    isbn = models.ForeignKey(Book, on_delete=models.CASCADE, db_column='isbn')
    t_time = models.DateTimeField(db_column='t_time')
    is_collected = models.BooleanField(db_column='is_collected', default = False)

    class Meta:
        unique_together = (('user_id', 'isbn'),)

class Stationery(models.Model):
    stationery_id = models.AutoField(db_column='stationery_id', primary_key=True)
    stationery_name = models.CharField(db_column='stationery_name', max_length = 50)
    tot_quantity = models.IntegerField(db_column='tot_quantity',validators=[MinValueValidator(1)], blank=True, null=True)
    location_id = models.ForeignKey(Location, on_delete = models.DO_NOTHING,db_column='location_id', null=True, blank=True)

class StationeryDonate(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    stationery_id = models.ForeignKey(Stationery, on_delete=models.CASCADE, db_column='stationery_id')
    t_time = models.DateTimeField(db_column='t_time')
    quantity = models.IntegerField(db_column='quantity', validators=[MinValueValidator(1)])
    is_collected = models.BooleanField(db_column='is_collected',default = False)

    class Meta:
        unique_together = (('user_id', 'stationery_id','t_time'),)

class Money(models.Model):
    money_id = models.AutoField(db_column='money_id', primary_key=True)  
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    t_time = models.DateTimeField(db_column='t_time')
    amount = models.IntegerField(db_column='amount')
    transaction_id = models.TextField(db_column='transaction_id', max_length=10, null=True)  

    class Meta:
        unique_together = (('money_id', 't_time'),)

    def __str__(self):
        """String for representing the Model object."""
        return str(self.money_id)