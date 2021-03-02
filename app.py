from flask import Flask, render_template, request,url_for,redirect, flash
import requests
from quotes import quotes
from flask_mail import Mail,Message

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Df_ongFEDG5f-51CquPmLdaKg9f5NgEWwQ'
app.config.from_pyfile('config.cfg')

mail = Mail(app)

@app.route('/',methods=['POST','GET'])
def index():
    data = {}
    if request.method == 'POST':
        try:
            city = request.form['city'].title()
            if not city :
                flash('Please enter a city')
                return redirect(url_for('index'))

            url = f'https://api.weatherbit.io/v2.0/forecast/daily?city={city}&key=e0ff2a6970ff41f09562937a434f1cd2'
            url2 = f'https://api.weatherbit.io/v2.0/forecast/daily?city={city}&units=i&key=e0ff2a6970ff41f09562937a434f1cd2'

            response = requests.get(url).json()
            response_F = requests.get(url2).json()

            data = {
                'city': city,
                'wind': round(response['data'][0]['wind_spd']),
                'windF': round(response_F['data'][0]['wind_spd']),
                'temperature': round(response['data'][0]['temp']),
                'temperatureF': round(response_F['data'][0]['temp']),
                'icon': [i['weather']['icon'] for i in response['data']],
                'description': response['data'][0]['weather']['description'],
                'wind_direction': response['data'][0]['wind_cdir'],
                'max_temp': [round(i['max_temp']) for i in response['data']],
                'min_temp': [round(i['min_temp']) for i in response['data']],
                'max_tempF': [round(i['max_temp']) for i in response_F['data']],
                'min_tempF': [round(i['min_temp']) for i in response_F['data']],
                'date': [i['valid_date'] for i in response['data']],
            }

        except:
            flash('City not found')
            return redirect(url_for('index'))

    return render_template('index.html',data=data,quotes=quotes)

@app.route('/contact',methods=['POST'])
def contact():
    if request.method == 'POST':
        email = request.form['email']
        msg = Message('Contact from Web App',recipients=['batomijovic@hotmail.com'])
        msg.body = f'You have contact from {email}'
        mail.send(msg)
        flash('Thank You for contacting me, i will reply to You soon')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
