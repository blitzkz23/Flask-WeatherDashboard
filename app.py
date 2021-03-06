import requests
import configparser
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def weather_dashboard():
    return render_template('home.html')

@app.route('/results', methods=['POST'])
def render_results():
    #get zip code fro html form
    zip_code = request.form['zipCode']

    #code below get the value from api's json
    api_key = get_api_key()
    data = get_weather_result(zip_code, api_key)
    temp = "{0:.2f}".format(data["main"]["temp"]) #get data from json key "main" "temp"
    feels_like = "{0:.2f}".format(data["main"]["feels_like"])
    weather = data["weather"][0]["main"]
    location = data["name"]

    return render_template('results.html',
                           location=location, temp=temp,
                           feels_like=feels_like, weather=weather)

def get_api_key():
    #this function to get the api from config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']

def get_weather_result(zip_code, api_key):
    api_url = "http://api.openweathermap.org/data/2.5/weather?zip={}&units=metric&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json() #return the api information in json format

if __name__ == '__main--': #ensure that your app only run once
    app.run(debug=True) #for debugging purpose so we dont have to restart the server everytime



print(get_weather_result("50261", get_api_key())) #call the api

