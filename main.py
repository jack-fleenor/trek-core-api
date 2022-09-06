import re
from bs4 import BeautifulSoup
import requests
import urllib

with open("index.html", "r", encoding='utf-8', errors='ignore') as f: # r = "Read" f = "File"
  doc = BeautifulSoup(f, "html.parser")

tags = doc.find_all("a")
filtered_tags = []
filtered_links = []

for tag in tags:
  if tag.text.startswith("Down"):
    filtered_tags.append(tag)
    filtered_links.append(tag.get("href"))
  else: continue

print(filtered_links)

for link in filtered_links:
  r = requests.get(link)
  with open("/documents", "wb") as f:
    f.write(r.content())