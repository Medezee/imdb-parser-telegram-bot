import re
import random
import imdbParser

def random_movie(url):
    text = imdbParser.get_movies_list(url)

    matcher_names = r'"title":"[ыэъйцукеннгшщзхїфівапролджєячсмитьбюЫЭЪЙЦУКЕНГШЩЗХЇФІВАПРОЛДЖЄЯЧСМИТЬБЮA-Za-z :0-9]+"'
    matcher_links = r'"href":"/title/tt[0-9]+"'

    titles = re.findall(pattern=matcher_names, string=text)
    href = re.findall(pattern=matcher_links, string=text)

    links = {}
    for movie, link in zip(titles,href):
        links['https://www.imdb.com'+link.split(':')[1].strip('"')] = movie.split(':')[1].strip('"')

    movie_link = random.choice(list(links.keys()))

    if not movie_link:
        return {'movie': '' , 'link': ''}
    else:
        return {'movie': links[movie_link] , 'link': movie_link}