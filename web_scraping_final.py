## Scraping Top Repositories for Topics on GitHub

! pip install requests  --quiet
import requests

topics_url = 'https://github.com/topics'
response = requests.get(topics_url)
response.status_code
len(response.text)
page_content = response.text
page_content[:500] 

with open('webpage.html', 'w') as f:
  f.write(page_content)

!pip install beautifulsoup4 --upgrade --quiet
from bs4 import BeautifulSoup
doc = BeautifulSoup(page_content, 'html.parser')

#  Getting topic titles.
attributevalue_title = "f3 lh-condensed mb-0 mt-1 Link--primary"
topic_title_p_tags = doc.find_all('p', {'class' : attributevalue_title})
len(topic_title_p_tags)
topic_title_p_tags[:5]

#  Getting topic description.
attributevalue_desc = "f5 color-fg-muted mb-0 mt-1"
topic_description_p_tags = doc.find_all('p', {'class' : attributevalue_desc })
topic_description_p_tags[:5]

#  getting first p tag : 3D
ptag_3D = topic_title_p_tags[0]
print(ptag_3D)
topic_url_a_tag = doc.find_all('a', {'class' : 'no-underline flex-grow-0'})
len(topic_url_a_tag)

# getting first a tag : 3D
atag_3D = topic_url_a_tag[0]['href']
print("http://github.com" + topic_url_a_tag[0]['href'])

topic_title_p_tags[0].text

topic_titles = []
for tag in topic_title_p_tags:
  topic_titles.append(tag.text)
print(topic_titles)

topic_descriptions = []
for tags in topic_description_p_tags:
  topic_descriptions.append(tags.text.strip())
print(topic_descriptions)

topic_URLS = []
for tag in topic_url_a_tag:
  topic_URLS.append('https://github.com'+tag['href'])
print(topic_URLS)

import pandas as pd

topics_dict = {'TITLE': topic_titles, 'DESCRIPTION': topic_descriptions, 'URL': topic_URLS}
topics_df = pd.DataFrame(topics_dict)
topics_df

topics_df.to_csv('GITHUBTOPICS.csv', index = None)

topic_page_url = topic_URLS[0]
topic_page_url

response = requests.get(topic_page_url)
response.status_code

topic_doc = BeautifulSoup(response.text, 'html.parser')

h3_attributevalue_repo = 'f3 color-fg-muted text-normal lh-condensed'
repo_tags = topic_doc.find_all('h3', {'class' : h3_attributevalue_repo})
len(repo_tags)

repo_tags[0]
a_tags = repo_tags[0].find_all('a')
a_tags

print(a_tags[0].text.strip())
print(a_tags[1].text.strip())
print(a_tags[1]['href'])

base_url = 'https://github.com'
repo_url = base_url + a_tags[1]['href']
print(repo_url)

star_tags = topic_doc.find_all('span', {'class' : 'Counter js-social-count' })
len(star_tags)

star_tags[0].text.strip()

def parse_star_count(stars_str):
  stars_str = stars_str.strip()
  if stars_str[-1] == 'k':
    return int(float(stars_str[:-1]) * 1000)
  return int(stars_str)

parse_star_count(star_tags[0].text.strip())

def get_repo_info(h3_tags, star_tags):
  #  returns all the required information about the repository
  a_tags = h3_tags.find_all('a')
  username = a_tags[0].text.strip()
  repo_name = a_tags[1].text.strip()
  repo_url = a_tags[1]['href']
  stars = parse_star_count(star_tags.text.strip())
  return username, repo_name, repo_url, stars

get_repo_info(repo_tags[0], star_tags[0])

topic_repos_dict = {'username' : [], 'repo_name' : [], 'stars' : [], 'repo_url' : []}
for i in range (len(repo_tags)):
  repo_info = get_repo_info(repo_tags[i], star_tags[i])
  topic_repos_dict['username'].append(repo_info[0])
  topic_repos_dict['repo_name'].append(repo_info[1])
  topic_repos_dict['repo_url'].append(repo_info[2])
  topic_repos_dict['stars'].append(repo_info[3])

topic_repos_df = pd.DataFrame(topic_repos_dict)
topic_repos_df

#  getting information about all the the repositories of a topic
import os
def get_topic_page(topic_url):
  response = requests.get(topic_url)

  if response.status_code != 200:
    raise Exception('Failed to load page {}'.format(topic_url))

  topic_doc = BeautifulSoup(response.text, 'html.parser')
  return topic_doc


def get_repo_info(h3_tags, star_tags):
  a_tags = h3_tags.find_all('a')
  username = a_tags[0].text.strip()
  repo_name = a_tags[1].text.strip()
  repo_url = a_tags[1]['href']
  stars = parse_star_count(star_tags.text.strip())
  return username, repo_name, repo_url, stars


def get_topic_repos(topic_doc):
  h3_attributevalue_repo = 'f3 color-fg-muted text-normal lh-condensed'
  repo_tags = topic_doc.find_all('h3', {'class' : h3_attributevalue_repo})

  star_tags = topic_doc.find_all('span', {'class' : 'Counter js-social-count' })

  topic_repos_dict = {'username' : [], 'repo_name' : [], 'stars' : [], 'repo_url' : []}
  for i in range (len(repo_tags)):
    repo_info = get_repo_info(repo_tags[i], star_tags[i])
    topic_repos_dict['username'].append(repo_info[0])
    topic_repos_dict['repo_name'].append(repo_info[1])
    topic_repos_dict['repo_url'].append(repo_info[2])
    topic_repos_dict['stars'].append(repo_info[3])

  return pd.DataFrame(topic_repos_dict)


def scrape_topic(topic_url, path):

  if os.path.exists(path):
    print('The file {} already  exists. Skip loading'.format(path))
    return
  topic_df = get_topic_repos(get_topic_page(topic_url))
  topic_df.to_csv(path, index = None)

url6 = topic_URLS[6]
topic6_doc = get_topic_page(url6)
topic6_repos = get_topic_repos(topic6_doc)
topic6_repos

topic_URLS[4]

get_topic_repos(get_topic_page(topic_URLS[4]))

get_topic_repos(get_topic_page(topic_URLS[4])).to_csv('df_to.csv', index = None)

def get_topic_titles(doc):
  attributevalue_title = "f3 lh-condensed mb-0 mt-1 Link--primary"
  topic_title_p_tags = doc.find_all('p', {'class' : attributevalue_title})
  topic_titles = []
  for tag in topic_title_p_tags:
    topic_titles.append(tag.text)
  return topic_titles

def get_topic_descs(doc):
  attributevalue_desc = "f5 color-fg-muted mb-0 mt-1"
  topic_description_p_tags = doc.find_all('p', {'class' : attributevalue_desc })
  topic_descriptions = []
  for tags in topic_description_p_tags:
    topic_descriptions.append(tags.text.strip())
  return topic_descriptions

def get_topic_urls(doc):
  topic_url_a_tag = doc.find_all('a', {'class' : 'no-underline flex-grow-0'})
  topic_URLS = []
  for tag in topic_url_a_tag:
    topic_URLS.append('https://github.com'+tag['href'])
  return topic_URLS

def scrape_topics():    # scrape for all topics all the top repository
  topic_url ='https://github.com/topics'
  response = requests.get(topics_url)
  if response.status_code != 200:
    raise Exception('Failed to load page {}'.format(topic_url))

  topics_dict = {'title' : get_topic_titles(doc),
                 'description' : get_topic_descs(doc),
                 'url' : get_topic_urls(doc)}
  return pd.DataFrame(topics_dict)

scrape_topics()

def scrape_topics_repos():
  print("Scraping list of topics--")
  topics_df = scrape_topics()

  os.makedirs('Data', exist_ok = True)

  for index, row in topics_df.iterrows():
    print('Scraping top repositories for "{}" '.format(row['title']))
    scrape_topic(row['url'], row['title'])

scrape_topics_repos()
