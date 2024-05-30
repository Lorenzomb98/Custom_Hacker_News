#importing necessary modules
import requests
from bs4 import BeautifulSoup
import pprint

#listing urls of first two pages of Hacker News
urls = ['https://news.ycombinator.com/','https://news.ycombinator.com/?p=2']

#acquiring links and subtext(for votes) of articles on page 1)
res = requests.get(urls[0])
soup = BeautifulSoup(res.content, 'html.parser')
links = soup.select('.titleline > a')
subtext = soup.select('.subtext')

#acquiring links and subtext(for votes) of articles on page 2)
res2 = requests.get(urls[1])
soup2 = BeautifulSoup(res2.content, 'html.parser')
links2 = soup2.select('.titleline > a')
subtext2 = soup2.select('.subtext')

#creating a superlist with information of both pages
super_links = links + links2
super_subtext = subtext + subtext2

#sorting articles by votes
def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key= lambda k:k['votes'],reverse=True)

#filtering articles by 100+ votes
def create_custom_hackernews(links,subtext):
    hn = []
    for index,item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[index].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points',''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
    return sort_stories_by_votes(hn)

pprint.pprint(create_custom_hackernews(super_links, super_subtext))