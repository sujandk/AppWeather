from django.shortcuts import render, redirect
from .models import City , Date , Time , Weather
import requests
from django.utils.timezone import now
from datetime import date as dt_date
from datetime import datetime, timezone
from pytz import timezone
import math
from django.db.models import Q
from django.http import HttpResponse
import csv
from django.contrib import messages


def home(request):
    if request.method == 'POST':
        try:
            city = request.POST['city']
            country = request.POST['country']
            api_key = '40b9e3b48771a8ec521f9fb68e2c918c'
            url = f'https://api.openweathermap.org/data/2.5/forecast?q={city},{country}&appid={api_key}&units=imperial'
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data.get('cod') != "200":  
                raise ValueError("City could not be found")
            lists = data['list']
            city_instance, created = City.objects.get_or_create(name=city, country=country)
      

            for list in lists:
                date = list['dt_txt'].split(' ')[0]
                time = list['dt_txt'].split(' ')[1]
                temperature = list['main']['temp']
                humidity = list['main']['humidity']
                feels_like = list['main']['feels_like']
                description = list['weather'][0]['description']
              
                date_obj = datetime.strptime(date, '%Y-%m-%d').date()

                time_obj = datetime.strptime(time, '%H:%M:%S').time()
            
            
                date_instance , created = Date.objects.get_or_create(date=date_obj , city=city_instance)
                time_instance , created = Time.objects.get_or_create(time=time_obj , date=date_instance)
                Weather.objects.get_or_create(
                date=date_instance , 
                city=city_instance ,
                time=time_instance ,
                temperature=temperature , 
                humidity=humidity , 
                feels_like=feels_like , 
                description=description)
        
            cityName = City.objects.get(name= city)
            dates = cityName.date_set.all()
            weather_data = {}
            for date in dates:
                related_times = date.time_set.all()
                weather_data[date] = []
                for time in related_times:
                    weather=Weather.objects.get(time=time)
        
                    weather_data[date].append({
                    "time": time.time.strftime('%H:%M:%S'),
                    "temperature": weather.temperature,
                    "humidity": weather.humidity,
                    "feels_like": weather.feels_like,
                    "description": weather.description,
                    })
        

            return render(request, 'base/forecast.html' , {'weather_date': weather_data , 'city': city})
        
        except requests.exceptions.RequestException as e:
            messages.error(request, f"An error occurred while connecting to the weather service: {e}")
        except ValueError as e:
            messages.error(request, str(e))
        except KeyError:
            messages.error(request, "The weather service returned unexpected data. Please try again.")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {e}")
     
   
   
   
   
   
   # until this point is the try and except block
   
   
    recent_searches = City.objects.all().order_by('-created_at')[:5]
    current_time = now()
    current_hour = current_time.hour
    closestHour =  math.ceil((current_hour/3))*3
    fetchingHour = f"{closestHour:02}:00:00"
    current_date = dt_date.today()
    weather_data = {}
    for search in recent_searches:
        city_weather = []
        dates = search.date_set.filter(date=current_date)
        for date in dates:

            #  timeAtCurrent = date.time_set.filter(time=fetchingHour)
            timeAtCurrent = date.time_set.filter(time=fetchingHour).first()  
        
            if timeAtCurrent:
                weather = Weather.objects.filter(time=timeAtCurrent).first()  
            
                if weather:
                # Print the weather data
                    city_weather.append({
                        'time': fetchingHour,
                        'temperature': weather.temperature,
                        'humidity': weather.humidity,
                        'feels_like': weather.feels_like,
                        'description': weather.description
                    })
                else:
                    city_weather.append({
                        'time': fetchingHour,
                        'temperature': 'N/A',
                        'humidity': 'N/A',
                        'feels_like': 'N/A',
                        'description': 'N/A'
                    })
            else:
               city_weather.append({
                    'time': fetchingHour,
                    'temperature': 'N/A',
                    'humidity': 'N/A',
                    'feels_like': 'N/A',
                    'description': 'N/A'
                })
  
            weather_data[search.name] = city_weather

    return render(request, "base/home.html", {'weather_data': weather_data})



def foreCast(request , city):
    cityName = City.objects.get(name= city)
    dates = cityName.date_set.all()
    weather_data = {}
    for date in dates:
        related_times = date.time_set.all()
        weather_data[date] = []
        for time in related_times:
            weather=Weather.objects.get(time=time)
        
            weather_data[date].append({
                    "time": time.time.strftime('%H:%M:%S'),
                    "temperature": weather.temperature,
                    "humidity": weather.humidity,
                    "feels_like": weather.feels_like,
                    "description": weather.description,
                })
    return render(request, "base/forecast.html" , {'weather_date': weather_data , 'city': cityName})

def savedCities(request):
    if request.method == 'POST':
        try:
            
            city = City.objects.get(name=request.POST['city'].lower())
        except City.DoesNotExist:
            return HttpResponse(f"City '{request.POST['city']}' not found in your saved database.")
      

        dates = city.date_set.all()
        weather_data = {}
        for date in dates:
            related_times = date.time_set.all()
            weather_data[date] = []
            for time in related_times:
                weather=Weather.objects.get(time=time)
                weather_data[date].append({
                "time": time.time.strftime('%H:%M:%S'),
                "temperature": weather.temperature,
                "humidity": weather.humidity,
                "feels_like": weather.feels_like,
                "description": weather.description,
                })
        return render(request, "base/forecast.html" , {'weather_date': weather_data , 'city': city})
    
    return redirect('home')
    
def delete(request , city):
    city = City.objects.get(name=city)
    if request.method == 'POST':
        city.delete()
        return redirect('home')
    return render(request, "base/delete.html" , {'object': city})

def exportWeather(request):
     # Create HttpResponse with content type as CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="weather_data.csv"'

    # Create a CSV writer
    writer = csv.writer(response)

    # Write the header row
    writer.writerow(['City', 'Country', 'Date', 'Time', 'Temperature', 'Humidity', 'Feels Like', 'Description'])

    # Fetch and write data from the database
    weather_data = Weather.objects.select_related('city', 'date', 'time')
    for weather in weather_data:
        writer.writerow([
            weather.city.name,
            weather.city.country,
            weather.date.date,
            weather.time.time.strftime('%H:%M:%S'),
            weather.temperature,
            weather.humidity,
            weather.feels_like,
            weather.description,
        ])
    return response