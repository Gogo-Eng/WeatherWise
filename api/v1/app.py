from flask import Flask, render_template, request, redirect, url_for
from api.v1.views import app_views  # type: ignore
import requests

app = Flask(__name__, template_folder='../../web_static/templates',
            static_folder='../../web_static/static')
app.register_blueprint(app_views, url_prefix="/")

@app.route('/')
def base():
    return render_template('base.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/submit_city', methods=['POST'])
def submit_city():
    city = request.form.get('city')
    return redirect(url_for('get_weather', city=city))

@app.route('/weather/<city>')
def get_weather(city):
    api_key = '442d038d4f21480a8f5155320240606'
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=2&aqi=no&alerts=no"
    response = requests.get(url)
    weather_data = response.json()
    
    if 'error' not in weather_data:
        weather = {
            'city': weather_data['location']['name'],
            'country': weather_data['location']['country'],
            'temperature': weather_data['current']['temp_c'],
            'condition': weather_data['current']['condition']['text'],
            'icon': weather_data['current']['condition']['icon'],
            'forecast': weather_data['forecast']['forecastday']
        }
        return render_template('result.html', weather=weather)
    else:
        return render_template('home.html', error='City not found')

if __name__ == '__main__':
    app.run(debug=True)