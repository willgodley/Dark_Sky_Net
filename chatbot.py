import aiml
import os
import requests
import json
import time
# Will Godley
# wmgodley

# kernel is responsible for responding to users
kernel = aiml.Kernel()

# load every aiml file in the 'standard' directory
dirname = 'aiml_data'
filenames = [os.path.join(dirname, f) for f in os.listdir(dirname)]
aiml_filenames = [f for f in filenames if os.path.splitext(f)[1]=='.aiml']

kernel = aiml.Kernel()
for filename in aiml_filenames:
    kernel.learn(filename)

# geocoding API key
geocodingAPIkey = 'AIzaSyCK2j0cGAT9mSndYY-N7jOISrC06hDRWcc'

# Dark sky net API key
darkSkyKey = 'bc5e0cf1c3558274c776fa47f86b5e47'

latLongCacheName = 'latLongCache.json'
weatherCacheName = 'weatherCache.json'

# Helper function that returns latitude and longitude of a city
def getLatLong(city):

    # Opens and reads cache or creates a new dictionary
    try:
        latLongCache = open(latLongCacheName, 'r')
        latLongContents = latLongCache.read()
        latLongCache.close()
        latLongDict = json.loads(latLongContents)
    except:
        latLongDict = {}

    fullRequest = 'https://maps.googleapis.com/maps/api/geocode/json?' + "adress=" + city + "key=" + geocodingAPIkey

    # Either uses data from cache or API call depending on if the data is in the cache
    try:
        if fullRequest not in latLongDict:
            geocodingResponse = requests.get('https://maps.googleapis.com/maps/api/geocode/json?', params = {
                'address' : city,
                'key' : geocodingAPIkey
                })
            latLongDict[fullRequest] = json.loads(geocodingResponse.text)
            latLongCache = open(latLongCacheName, 'w')
            latLongCache.write(json.dumps(latLongDict))
            latLongCache.close()
            data = latLongDict[fullRequest]
        else:
            data = latLongDict[fullRequest]
    except:
        return 'Internet fail'

    # Checks that the API call worked correctly
    if data['status'] != 'OK':
        return 'Google fail'
    # Ensures that results are for city, not an address
    elif data['results'][0]['address_components'][0]['types'][0] != 'locality':
        return 'Google fail'

    lat_lon_data = data['results'][0]['geometry']['location']
    latitude = str(lat_lon_data['lat'])
    longitude = str(lat_lon_data['lng'])

    return (latitude, longitude)

# Helper function that returns weather data in json format
def getWeatherData(lat, lng):

    # Opens and reads cache or creates a new dictionary
    try:
        weatherCache = open(weatherCacheName, 'r')
        weatherContents = weatherCache.read()
        weatherCache.close()
        weatherDict = json.loads(weatherContents)
    except:
        weatherDict = {}

    location = lat + ', ' + lng
    fullRequest = 'https://api.darksky.net/forecast/' + darkSkyKey + '/' + location

    # Either uses data from cache or API call depending on if the data is in the cache
    if fullRequest not in weatherDict:
        try:
            weatherResponse = requests.get('https://api.darksky.net/forecast/' + darkSkyKey + '/' + location)
            weatherData = json.loads(weatherResponse.text)
        except:
            return 'Internet fail'
        weatherDict[fullRequest] = weatherData
        weatherCache = open(weatherCacheName, 'w')
        weatherCache.write(json.dumps(weatherDict))
        weatherCache.close()
        data = weatherDict[fullRequest]

    else:
        if time.time() > (weatherDict[fullRequest]['currently']['time'] + (5*60)):
            try:
                weatherResponse = requests.get('https://api.darksky.net/forecast/' + darkSkyKey + '/' + location)
                weatherData = json.loads(weatherResponse.text)
            except:
                return 'Internet fail'
            weatherDict[fullRequest] = weatherData
            weatherCache = open(weatherCacheName, 'w')
            weatherCache.write(json.dumps(weatherDict))
            weatherCache.close()
            data = weatherDict[fullRequest]
        else:
            data = weatherDict[fullRequest]


    # Check that API call worked correctly
    if 'error' in data:
        return 'Dark Sky fail'

    return data

# Response for getting current weather
def currentWeather(city):
    weather = getCurrentWeather(city)

    if weather == 'Google fail':
        return 'Is {} a city?'.format(city)
    elif weather == 'Dark Sky fail':
        return 'Sorry, I don\'t know'
    elif weather == 'Internet fail':
        return 'Make sure you are connected to the internet'
    else:
        temperature = weather[0]
        skies = weather[1]
        return 'In {}, it is {} and {}'.format(city, temperature, skies)

# Gets current weather for a city passed in
def getCurrentWeather(city):
    lat_lon_data = getLatLong(city)

    if lat_lon_data == 'Google fail':
        return 'Google fail'
    elif lat_lon_data == 'Internet fail':
        return 'Internet fail'

    latitude = lat_lon_data[0]
    longitude = lat_lon_data[1]
    data = getWeatherData(latitude, longitude)

    if data == 'Dark Sky fail':
        return 'Dark Sky fail'
    elif data == 'Internet fail':
        return 'Internet fail'
    else:
        temperature = data['currently']['temperature']
        skies = data['currently']['summary']
        return (temperature, skies)

# Response for asking for daily high in a city
def highOfDay(city):
    high = getHighofDay(city)

    if high == 'Google fail':
        return 'Is {} a city?'.format(city)
    elif high == 'Dark Sky fail':
        return 'Sorry, I don\'t know'
    elif high == 'Internet fail':
        return 'Make sure you are connected to the internet'
    else:
        return 'In {}, it will reach {} degrees Fahrenheit today'.format(city, high)

# Gets the high of the day for a city
def getHighofDay(city):
    lat_lon_data = getLatLong(city)

    if lat_lon_data == 'Google fail':
        return 'Google fail'
    elif lat_lon_data == 'Internet fail':
        return 'Internet fail'

    latitude = lat_lon_data[0]
    longitude = lat_lon_data[1]
    data = getWeatherData(latitude, longitude)

    if data == 'Dark Sky fail':
        return 'Dark Sky fail'
    elif data == 'Internet fail':
        return 'Internet fail'

    high = str(data['daily']['data'][0]['temperatureHigh'])

    return high

# Response for getting the daily low in a city
def lowOfDay(city):
    low = getLowofDay(city)

    if low == 'Google fail':
        return 'Is {} a city?'.format(city)
    elif low == 'Dark Sky fail':
        return 'Sorry, I don\'t know'
    elif low == 'Internet fail':
        return 'Make sure you are connected to the internet'
    else:
        return 'In {}, the low will be {} degrees Fahrenheit today'.format(city, low)

# Gets the low temp of the day for a city
def getLowofDay(city):
    lat_lon_data = getLatLong(city)

    if lat_lon_data == 'Google fail':
        return 'Google fail'
    elif lat_lon_data == 'Internet fail':
        return 'Internet fail'

    latitude = lat_lon_data[0]
    longitude = lat_lon_data[1]
    data = getWeatherData(latitude, longitude)

    if data == 'Dark Sky fail':
        return 'Dark Sky fail'
    elif data == 'Internet fail':
        return 'Internet fail'

    low = str(data['daily']['data'][0]['temperatureLow'])

    return low

# Response for the high temperature in a week
def highOfWeek(city):
    highTemp = getHighofWeek(city)

    if highTemp == 'Google fail':
        return 'Is {} a city?'.format(city)
    elif highTemp == 'Dark Sky fail':
        return 'Sorry, I don\'t know'
    elif highTemp == 'Internet fail':
        return 'Make sure you are connected to the internet'
    else:
        return 'In {}, it will reach {} degrees Fahrenheit this week'.format(city, highTemp)

# Gets the high temperature of the week in a city
def getHighofWeek(city):
    lat_lon_data = getLatLong(city)

    if lat_lon_data == 'Google fail':
        return 'Google fail'
    elif lat_lon_data == 'Internet fail':
        return 'Internet fail'

    latitude = lat_lon_data[0]
    longitude = lat_lon_data[1]
    data = getWeatherData(latitude, longitude)

    if data == 'Dark Sky fail':
        return 'Dark Sky fail'
    elif data == 'Internet fail':
        return 'Internet fail'

    weekData = data['daily']['data']

    highs = []
    for a in range(7):
        highs.append(weekData[a]['temperatureHigh'])
    highs = sorted(highs, key = lambda x: x, reverse = True)
    highOfWeek = highs[0]

    return highOfWeek

# Response for low of the week in a city
def lowOfWeek(city):
    lowTemp = getLowofWeek(city)

    if lowTemp == 'Google fail':
        return 'Is {} a city?'.format(city)
    elif lowTemp == 'Dark Sky fail':
        return 'Sorry, I don\'t know'
    elif lowTemp == 'Internet fail':
        return 'Make sure you are connected to the internet'
    else:
        return 'In {}, the low will be {} degrees Fahrenheit this week'.format(city, lowTemp)

# Gets the low of the week in a city
def getLowofWeek(city):
    lat_lon_data = getLatLong(city)

    if lat_lon_data == 'Google fail':
        return 'Google fail'
    elif lat_lon_data == 'Internet fail':
        return 'Internet fail'

    latitude = lat_lon_data[0]
    longitude = lat_lon_data[1]
    data = getWeatherData(latitude, longitude)

    if data == 'Dark Sky fail':
        return 'Dark Sky fail'
    elif data == 'Internet fail':
        return 'Internet fail'

    weekData = data['daily']['data']

    lows = []
    for a in range(7):
        lows.append(weekData[a]['temperatureLow'])
    lows = sorted(lows, key = lambda x: x)
    lowOfWeek = lows[0]

    return lowOfWeek

# Response for chances of rain in a dat
def rainInADay(city):
    dayProbability = computeDayRainProbability(city)

    if dayProbability == 'Google fail':
        return 'Is {} a city?'.format(city)
    elif dayProbability == 'Dark Sky fail':
        return 'Sorry, I don\'t know'
    elif dayProbability == 'Internet fail':
        return 'Make sure you are connected to the internet'

    if dayProbability < 0.1:
        return 'It almost definitely will not rain in {}'.format(city)
    elif dayProbability >= 0.1 and probability < 0.5:
        return 'It probably will not rain in {} this week'.format(city)
    elif dayProbability >= 0.5 and probability < 0.9:
        return 'It probably will rain in {} this week'.format(city)
    elif dayProbability >= 0.9:
        return 'It will almost definitely rain in {} today'.format(city)

# Get the probability of rain in a day
def computeDayRainProbability(city):
    lat_lon_data = getLatLong(city)

    if lat_lon_data == 'Google fail':
        return 'Google fail'
    elif lat_lon_data == 'Internet fail':
        return 'Internet fail'

    latitude = lat_lon_data[0]
    longitude = lat_lon_data[1]
    data = getWeatherData(latitude, longitude)

    if data == 'Dark Sky fail':
        return 'Dark Sky fail'
    elif data == 'Internet fail':
        return 'Internet fail'

    probability = data['daily']['data'][0]['precipProbability']

    return probability

# Statements for chance of rain this week
def rainInAWeek(city):
    probability = computeWeekRainProbability(city)

    if probability == 'Google fail':
        return 'Is {} a city?'.format(city)
    elif probability == 'Dark Sky fail':
        return 'Sorry, I don\'t know'
    elif probability == 'Internet fail':
        return 'Make sure you are connected to the internet'

    if probability < 0.1:
        return 'It almost definitely will not rain in {}'.format(city)
    elif probability >= 0.1 and probability < 0.5:
        return 'It probably will not rain in {} this week'.format(city)
    elif probability >= 0.5 and probability < 0.9:
        return 'It probably will rain in {} this week'.format(city)
    elif probability >= 0.9:
        return 'It will almost definitely rain in {} this week'.format(city)


# Computes the probability that it will rain at least once this week in a city
def computeWeekRainProbability(city):
    lat_lon_data = getLatLong(city)

    if lat_lon_data == 'Google fail':
        return 'Google fail'
    elif lat_lon_data == 'Internet fail':
        return 'Internet fail'

    latitude = lat_lon_data[0]
    longitude = lat_lon_data[1]
    data = getWeatherData(latitude, longitude)

    if data == 'Dark Sky fail':
        return 'Dark Sky fail'
    elif data == 'Internet fail':
        return 'Internet fail'

    weekData = data['daily']['data']

    probabilities_of_no_rain = []
    for a in range(7):
        probabilities_of_no_rain.append(1.0 - weekData[a]['precipProbability'])
    totalProbability = 1.0
    for a in probabilities_of_no_rain:
        totalProbability = totalProbability * a
    probability = 1 - totalProbability

    return probability

# Adding all kernel patterns
kernel.addPattern('What\'s the weather like in {city}?', currentWeather)
kernel.addPattern('How hot will it get in {city} today?', highOfDay)
kernel.addPattern('How cold will it get in {city} today?', lowOfDay)
kernel.addPattern('How hot will it get in {city} this week?', highOfWeek)
kernel.addPattern('How cold will it get in {city} this week?', lowOfWeek)
kernel.addPattern("is it going to rain in {city} today", rainInADay)
kernel.addPattern("is it going to rain in {city} this week", rainInAWeek)


q = input('> ')
while q != 'quit':
     print('{}\n'.format(kernel.respond(q)))
     # Get next input
     q = input('> ')
