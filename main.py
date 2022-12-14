from bs4 import BeautifulSoup, NavigableString
import requests

headers = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET',
  'Access-Control-Allow-Headers': 'Content-Type',
  'Access-Control-Max-Age': '3600',
  'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}

def get_series_urls(homepage):
  req = requests.get(homepage, headers=headers)
  soup = BeautifulSoup(req.content, 'html.parser')
  links_list = soup.find('ul', {'id': 'navbar'})
  links = links_list.find_all('li')
  results = []
  for link in links:
    hrefs = link.find_all('a')
    for href in hrefs:
      if href.text == 'Episode Guide':
        link = href['href'].rsplit('/episodes', 1)[0]
        results.append(f"{link}/episodes/")
  return results

def get_episode_links(series):
  print(f"getting links to series episodes...{series}")
  req = requests.get(series, headers=headers)
  soup = BeautifulSoup(req.content, 'html.parser')
  results = soup.find_all("td", {"class": "col2"})
  episode_links = []
  for result in results:
    for link in result.find_all("a", href=True):
      episode_links.append(link['href'])
  if len(episode_links) > 0:
    return episode_links
  else:
    return ["Error"]

def get_characters(episodes):
  print("generating characters...")
  characters = []
  for episode in episodes:
    episode_page = requests.get(episode, headers=headers)
    soup = BeautifulSoup(episode_page.content, 'html.parser')
    if soup.find("a", text="MAIN CHARACTERS"):
      print(episode)
      if 'index' in episode:
        page = episode.replace('index', 'main')
        episode_characters = scrape_characters_page(page)
      else:
        episode_characters = scrape_characters_page(f"{episode}main.html")
      for character in episode_characters:
        characters.append(character)
    if soup.find("a", text="GUEST CHARACTERS"):
      print(episode)
      if 'index' in episode:
        page = episode.replace('index', 'guests')
        episode_characters = scrape_characters_page(page)
      else:
        episode_characters = scrape_characters_page(f"{episode}guests.html")
      for character in episode_characters:
        characters.append(character)
  return characters

def scrape_characters_page(characters_page_url):
  print(f"scraping characters page {characters_page_url}", end="\r")
  results = []
  characters_page = requests.get(characters_page_url, headers=headers)
  soup = BeautifulSoup(characters_page.content, 'html.parser')
  table = soup.find("table", { "id":"AutoNumber60" })
  if table is not None:
    for row in table:
      if isinstance(row, NavigableString):
        continue
      table_datas = row.find_all('td')
      img = table_datas[0].find('img')
      name = table_datas[1].find('font')
      character = {}
      if name is not None:
        character['name'] = name.text.strip()
        if img is not None:
          character['image'] = f"{characters_page_url.rsplit('/', 1)[0]}/{img['src']}"
      if character != {}:
        if character['name'] == '' and img is not None:
          character['name'] = img['src'].rsplit('-', 1)[1]
          character['name'] = character['name'].rsplit('.', 1)[0]
        results.append(character)
    return results
  else:
    print(f"Table is empty... %s" % characters_page_url)

# series_urls_raw = get_series_urls("https://www.trekcore.com/")
# series_urls = [*set(series_urls_raw)]

# for series_url in series_urls:
#   print(f"checking series {series_url}")
#   episodes = get_episode_links(series_url)
#   print(f"this series has {len(episodes)} episodes")
#   if episodes is not None: 
#     characters = get_characters(episodes)
#     print(f"{series_url} has {len(characters)} characters.")
series_url = "https://tas.trekcore.com/episodes"
episodes = get_episode_links(series_url)
print(f"this series has {len(episodes)} episodes")
characters = get_characters(episodes)
print(f"{series_url} has {len(characters)} characters.")