import requests
import re
from aiogram import executor, Dispatcher, Bot, types

bot = Bot(token='6623223617:AAF8s_Rz0jt8b3hBCBqIdJQfxdCpa7ge8DM')
dp = Dispatcher(bot=bot)

def valid_ip(ip):
    aa = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",ip)
    if aa:
        return True
    else:
        return False
    
def get_info_by_ip(ip="127.0.0.1"):
    try:
        response = requests.get(url=f'http://ip-api.com/json/{ip}').json()
        info_ip = {}
        info_ip['IP'] = response['query']        
        info_ip['Country'] = response['country']
        info_ip['RegionName'] = response['regionName']
        info_ip['City'] = response['city']
        info_ip['zip'] = response['zip']
        info_ip['Lat'] = response['lat']
        info_ip['Lon'] = response['lon']

        text = ''
        for k,v in info_ip.items():
            text += k + ': ' + str(v) + '\n'
        return text

    except requests.exceptions.ConnectionError:
        return('[!] Please check your connection!')

def main():
    ip = input('Please enter a target IP: ')

    get_info_by_ip(ip=ip)
    
@dp.message_handler(commands=['start'])
async def start_command(message:types.Message): 
    text = 'Hello, ' + message.from_user.first_name + '!!' + '\n' + 'That bot can send you info about IP!\n' + 'Try send IP address for check!!'
    await message.answer(text = text)

@dp.message_handler(content_types=['text'])
async def send_info(message: types.Message):
    if valid_ip(message.text):
        await message.answer(text = get_info_by_ip(message.text))
    else:
        await message.answer(text = 'Not corrent IP, try again!')

if __name__ == "__main__":
    executor.start_polling(dispatcher=dp)