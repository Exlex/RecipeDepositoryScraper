import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup

def scrape():
	page = requests.get('https://www.therecipedepository.com/')
	soup = BeautifulSoup(page.text, 'html.parser')


	recipe_container = soup.find(class_='small-12 medium-6 large-6 columns')

	name = recipe_container.find(class_='recipe-name').string
	if name in recipes:
		return 0
	recipes[name] = 0
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




	directions = recipe_container.find(class_='directions').get_text('\n', strip=True).replace('Directions', '').strip().splitlines()
	for instruction in directions:
		print(instruction)


	post_data = {
		'name' : name,
		'img_url' : img_url,
		'ingredients' : ingredients_list,
		'directions' : directions
	}

	return post_data



recipes = {}
settings = open('settings.cfg', 'r')
client = MongoClient(settings.readline().strip())
settings.close()
db = client['myDb']

number_of_recipes = 100 # how many recipes to scrape

while(number_of_recipes > 0):
	print('Scrapes left:' + str(number_of_recipes-1))
	post_data = scrape()
	if post_data:
		result = db.recipes.insert_one(post_data)

	
	number_of_recipes -= 1

