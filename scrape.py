import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

#connect('mongodb+srv://dbadmin:knigareceptov96@cluster0.mongodb.net/myDb?retryWrites=true')
#connect(
#	db='myDb',
#	username='dbadmin',
#	password='knigareceptov96',
#	host='mongodb://dbadmin:knigareceptov96@cluster0.mongodb.net/myDb?retryWrites=true')
db_srv_url = open('settings.cfg', 'r').readline().strip()
client = MongoClient(db_srv_url)
db = client['myDb']

page = requests.get('https://www.therecipedepository.com/')
soup = BeautifulSoup(page.text, 'html.parser')


recipe_container = soup.find(class_='small-12 medium-6 large-6 columns')

name = recipe_container.find(class_='recipe-name').string
print(name)

img_url = recipe_container.find(class_='recipe-image row')['src']
print('\n'+img_url+'\n')

ingredients = recipe_container.findAll(class_='ingredient')
ingredients_list = []
if(len(ingredients) == 0):
	# old style of ingredients, using other method
	ingredients_list = recipe_container.find(class_='ingredients').get_text('\n', strip=True).replace('Ingredients', '').strip().splitlines()
else:
	ingredients_list = [ingredient.string for ingredient in ingredients]

for ingredient in ingredients_list:
		print(ingredient)




directions = recipe_container.find(class_='directions').get_text('\n\n', strip=True).replace('Directions', '').strip()
print('\n'+directions+'\n')


post_data = {
	'name' : name,
	'img_url' : img_url,
	'ingredients' : ingredients_list,
	'directions' : directions
}

result = db.recipes.insert_one(post_data)
print(result)