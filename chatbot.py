import requests

# API_ENDPOINT = 'https://flask-production-e09a.up.railway.app/chat'
API_ENDPOINT = 'http://localhost:5000/chat'

def send_message(message):
    data = {'message': message}
    response = requests.post(API_ENDPOINT, data=data)
    return response.json()['response']

while True:
    user_input = input('👨‍🦰 Kamu: ')
    response = send_message(user_input)
    print('🤖 HealthBot:', response, '\n')
    if user_input == 'quit':
        break