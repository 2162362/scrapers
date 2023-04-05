import requests
import os
from time import sleep
from bs4 import BeautifulSoup
from random import randint

base_url = 'https://www.zerozero.pt/player.php?id='
folder_path = '/mnt/mitsai/boss/pictures/zerozero_players'
start_id = 1
end_id = 100

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

for player_id in range(start_id, end_id + 1):
    url = base_url + str(player_id)
    response = requests.get(url, headers=headers)

    # Check if URL was redirected or if there was an error
    if response.history or response.status_code != 200:
        print(f'Error:Skipping player ID {player_id}')
        continue

    soup = BeautifulSoup(response.text, 'html.parser')

    logo_div = soup.find('div', {'class': 'logo'})
    player_image = logo_div.find('img')

    # Check if player image was found
    if not player_image:
        print(f'Error:Player image not found for id {player_id}')
        continue

    image_url = player_image['src']

    # Download and save the image
    image_response = requests.get(image_url)
    filename = os.path.join(folder_path, f'player_{player_id}.jpg')
    with open(filename, 'wb') as f:
        f.write(image_response.content)
    print(image_url)

    sleep_time = randint(10, 25) # randomize sleep time between 1 and 5 seconds
    sleep(sleep_time)
