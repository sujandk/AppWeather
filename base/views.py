from django.shortcuts import render
from .models import City , Date , Time , Weather
import requests

# Create your views here.
def home(request):
     if request.method == 'POST':
        city = request.POST['city']
        country = request.POST['country']
        api_key = '40b9e3b48771a8ec521f9fb68e2c918c'
        url = f'https://api.openweathermap.org/data/2.5/forecast?q={city},{country}&appid={api_key}'
        response = requests.get(url)
        data = response.json()
        lists = data['list']
        city_instance, created = City.objects.get_or_create(name=city, country=country)
      

        for list in lists:
            date = list['dt_txt'].split(' ')[0]
            time = list['dt_txt'].split(' ')[1]
            temperature = list['main']['temp']
            humidity = list['main']['humidity']
            feels_like = list['main']['feels_like']
            description = list['weather'][0]['description']
            from datetime import datetime
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
               
                
            
        
        # all_times = dates.time.all()
        # weather_data = {}

        # for date in dates:
        #     times_with_weather = date.times.all().prefetch_related('weather')  # `related_name="times"` is used here
        #     weather_data[date.date] = [{
        #     "time": time.time.strftime('%H:%M:%S'),
        #     "temperature": time.weather.temperature,
        #     "humidity": time.weather.humidity,
        #     "feels_like": time.weather.feels_like,
        #     "description": time.weather.description,
        #      }
        #     for time in times_with_weather
        #     ]
        

        return render(request, 'base/forecast.html' , {'weather_date': weather_data , 'city': city})
     
     recent_searches = City.objects.all()
     print(recent_searches)

     return render(request, "base/home.html")



