import requests
from bs4 import BeautifulSoup

def get_movies_list(url):
    data = requests.get(url)
    soup = BeautifulSoup(data.text,'html.parser')
    results = soup.find_all('span', attrs={'class':'ab_widget'})
    text = results[0].find('script')
    return text.text

if __name__ == "__main__":
    url = input('Enter your movie watchlist url: ')
    print(get_movies_list(url))