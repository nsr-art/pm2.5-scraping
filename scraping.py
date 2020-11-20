import request
from bs4 import BeautifulSoup

search = "weather in Bangkok"
URL = f"https://www.google.com/search?q={search}"

req = request.get(URL)
sav = BeautifulSoup(req.text,"html.parser")
update = sav.find("div",class="BNeawe").text
print(update)