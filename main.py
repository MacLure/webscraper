from bs4 import BeautifulSoup
import requests

sections = [
  "international",
  "politique",
  "societe",
  "planete",
  "climat",
  "afrique",
  "les-decodeurs",
  "sport",
  "education",
  "sante",
  "intimites",
  "campus",
  "sciences",
  "pixels",
  "disparitions",
  "le-fil-good",
  "le-monde-et-vous"
]

sections_str = "\n".join(sections)

section = ''

while section not in sections:
  print(f'Please select a news section:\n{sections_str}')
  section = input('> ')

def write_file(article, index):
  with open(f'articles/{index}.txt', 'w') as f:
    link = article['href']
    headline = article.find('h3', class_ = 'teaser__title').text.strip()
    article_page_text = requests.get(link).text
    article_soup = BeautifulSoup(article_page_text, 'lxml')
    description = article_soup.find('p', class_="article__desc")
    author = article_soup.find('a', class_="article__author-link")
    published_at = article_soup.find('section', class_="meta__date meta__date--header")
    read_time = article_soup.find('p', class_="meta__reading-time--header")
    paragraphs = article_soup('p', class_ = 'article__paragraph') 

    f.write(f'{headline}\n')
    f.write(f'{link}\n')
    if description:
      f.write(f'{description.text.strip()}\n')
    if author:
      f.write(f'{author.text.strip()}\n')
    if read_time:
      f.write(f'{read_time.text.strip()}\n')
    if published_at:
      f.write(f'{published_at.text.strip()}\n')
    for index, paragraph in enumerate(paragraphs):
      f.write(f'{paragraph.text.strip()}\n\n')

html_text = requests.get(f'https://www.lemonde.fr/{section}/').text
soup = BeautifulSoup(html_text, 'lxml')
articles = soup.find_all('a', class_ = 'teaser__link')

for index, article in enumerate(articles):
  write_file(article, index)
  print(f'file saved: {index}')
