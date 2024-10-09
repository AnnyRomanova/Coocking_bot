import requests
from bs4 import BeautifulSoup


url_egg = "https://www.russianfood.com/search/simple/index.php?ssgrtype=bytype&sskw_title=%E7%E0%E2%F2%F0%E0%EA&tag_tree%5B1%5D%5B%5D=0&tag_tree%5B2%5D%5B%5D=0&sskw_iplus=%FF%E9%F6%EE&sskw_iminus=&submit=#beforesearchform"
response_egg = requests.get(url_egg)
soup_egg = BeautifulSoup(response_egg.text, "lxml")
recipes_cards_egg_list = soup_egg.find_all("td", class_="rcp_wi_title")

egg_list = []
for recipe_card in recipes_cards_egg_list[:5]:
    tmp_list = []
    name = recipe_card.find("a").text.replace("\n", "")
    tmp_list.append(name)
    recipe_url = "https://www.russianfood.com" + recipe_card.find("a").get("href")
    tmp_list.append(recipe_url)
    tmp_list.append("яйцо, яйца")
    tmp_list.append("admin")
    egg_list.append(tuple(tmp_list))



url_bread = "https://www.russianfood.com/search/simple/index.php?ssgrtype=bytype&sskw_title=%E7%E0%E2%F2%F0%E0%EA&tag_tree%5B1%5D%5B%5D=0&tag_tree%5B2%5D%5B%5D=0&sskw_iplus=%F5%EB%E5%E1&sskw_iminus=&submit=#beforesearchform"
response_bread = requests.get(url_bread)
soup_bread = BeautifulSoup(response_bread.text, "lxml")
recipes_cards_bread_list = soup_bread.find_all("td", class_="rcp_wi_title")

bread_list = []
for recipe_card in recipes_cards_bread_list[:5]:
    tmp_list = []
    name = recipe_card.find("a").text.replace("\n", "")
    tmp_list.append(name)
    recipe_url = "https://www.russianfood.com" + recipe_card.find("a").get("href")
    tmp_list.append(recipe_url)
    tmp_list.append("хлеб")
    tmp_list.append("admin")
    bread_list.append(tuple(tmp_list))



url_sausage = "https://www.russianfood.com/search/simple/index.php?ssgrtype=bytype&sskw_title=%E7%E0%E2%F2%F0%E0%EA&tag_tree%5B1%5D%5B%5D=0&tag_tree%5B2%5D%5B%5D=0&sskw_iplus=%F1%EE%F1%E8%F1%EA%E8&sskw_iminus=&submit=#beforesearchform"
response_sausage = requests.get(url_sausage)
soup_sausage = BeautifulSoup(response_sausage.text, "lxml")
recipes_cards_sausage_list = soup_sausage.find_all("td", class_="rcp_wi_title")

sausage_list = []
for recipe_card in recipes_cards_sausage_list[:5]:
    tmp_list = []
    name = recipe_card.find("a").text.replace("\n", "")
    tmp_list.append(name)
    recipe_url = "https://www.russianfood.com" + recipe_card.find("a").get("href")
    tmp_list.append(recipe_url)
    tmp_list.append("сосиска, сосиски")
    tmp_list.append("admin")
    sausage_list.append(tuple(tmp_list))



url_tomato = "https://www.russianfood.com/search/simple/index.php?ssgrtype=bytype&sskw_title=%E7%E0%E2%F2%F0%E0%EA&tag_tree%5B1%5D%5B%5D=0&tag_tree%5B2%5D%5B%5D=0&sskw_iplus=%EF%EE%EC%E8%E4%EE%F0&sskw_iminus=&submit=#beforesearchform"
response_tomato = requests.get(url_tomato)
soup_tomato = BeautifulSoup(response_tomato.text, "lxml")
recipes_cards_tomato_list = soup_tomato.find_all("td", class_="rcp_wi_title")

tomato_list = []
for recipe_card in recipes_cards_tomato_list[:3]:
    tmp_list = []
    name = recipe_card.find("a").text.replace("\n", "")
    tmp_list.append(name)
    recipe_url = "https://www.russianfood.com" + recipe_card.find("a").get("href")
    tmp_list.append(recipe_url)
    tmp_list.append("помидор, помидоры, томат, томаты")
    tmp_list.append("admin")
    tomato_list.append(tuple(tmp_list))



url_sausage2 = "https://www.russianfood.com/search/simple/index.php?ssgrtype=bytype&sskw_title=%E7%E0%E2%F2%F0%E0%EA&tag_tree%5B1%5D%5B%5D=0&tag_tree%5B2%5D%5B%5D=0&sskw_iplus=%EA%EE%EB%E1%E0%F1%E0&sskw_iminus=&submit=#beforesearchform"
response_sausage2 = requests.get(url_sausage2)
soup_sausage2 = BeautifulSoup(response_sausage2.text, "lxml")
recipes_cards_sausage2_list = soup_sausage2.find_all("td", class_="rcp_wi_title")

sausage2_list = []
for recipe_card in recipes_cards_sausage2_list[:5]:
    tmp_list = []
    name = recipe_card.find("a").text.replace("\n", "")
    tmp_list.append(name)
    recipe_url = "https://www.russianfood.com" + recipe_card.find("a").get("href")
    tmp_list.append(recipe_url)
    tmp_list.append("колбаса")
    tmp_list.append("admin")
    sausage2_list.append(tuple(tmp_list))


url_cheese = "https://eda.ru/recepty/zavtraki"
response_cheese = requests.get(url_cheese)
soup_cheese = BeautifulSoup(response_cheese.text, "lxml")
recipes_cards_cheese_list = soup_cheese.find_all("div", class_="emotion-1j5xcrd")


cheese_list = []
for recipe_card in recipes_cards_cheese_list[:5]:
    tmp_list = []
    name = recipe_card.find("span", class_="emotion-1bs2jj2").text.replace("\n", "")
    tmp_list.append(name)
    recipe_url = "https://eda.ru/" + recipe_card.find("a").get("href")
    tmp_list.append(recipe_url)
    tmp_list.append("сыр")
    tmp_list.append("admin")
    cheese_list.append(tuple(tmp_list))