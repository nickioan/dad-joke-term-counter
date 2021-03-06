
import requests
from requests.exceptions import HTTPError
from djranker import word_count

def get_jokes(word_counter):
    url = 'https://icanhazdadjoke.com/'
    try:
        res = requests.get(url, headers={"Accept": "application/json"})
        res.raise_for_status()
        jsonRes = res.json()
        joke = jsonRes['joke']
        word_counter.add_joke(joke)      
    except HTTPError as http_err:
        print('HTTP error occured: {}'.format(http_err))
    except Exception as err:
        print('Other error occured: {}'.format(err))
    return
