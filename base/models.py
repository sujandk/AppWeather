from django.db import models
from django.utils.timezone import now

# Create your models here.
from django.db import models

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=255 , null=False , blank=False)
    country = models.CharField(max_length=255 , null=False , blank=False)
    created_at = models.DateTimeField( auto_now_add=True)  # Add default for migration

    def __str__(self):
        return self.name

class Date(models.Model):
    date = models.DateField(null=False , blank=False)
    city = models.ForeignKey(City , on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date}" 
    

class Time(models.Model):
    time = models.TimeField(null=False, blank=False)
    date = models.ForeignKey(Date, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.time.strftime('%H:%M:%S')}"  # Returns time in HH:MM:SS formats

class Weather(models.Model):
    date = models.ForeignKey(Date , on_delete=models.CASCADE)
    city = models.ForeignKey(City , on_delete=models.CASCADE)
    time = models.ForeignKey(Time, on_delete=models.CASCADE) 
    temperature = models.FloatField(null=False , blank=False)
    humidity = models.TextField(null=False , blank=False)
    feels_like = models.TextField(null=False , blank=False)
    description = models.TextField(null=False , blank=False)
   

    def __str__(self):
        return f"{self.temperature}-{self.humidity}-{self.feels_like}-{self.description}" 

