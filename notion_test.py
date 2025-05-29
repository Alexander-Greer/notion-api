from notion_client import NotionClient, NotionPage, NotionDatabaseEntry
# https://pypi.org/project/movieposters/
import movieposters as mp
from pull_recipe import scrape_me

# https://pypi.org/project/ingredient-parser-nlp/
from ingredient_parser.parsers import parse_ingredient

# DONT PUBLISH THESE
# API Testing Database
# https://www.notion.so/315f9b2914cc4b618e242dcb0d344d94?v=bccf5f925dd142c8bbaebdf34a32d047&pvs=4
# DATABASE_ID = "315f9b2914cc4b618e242dcb0d344d94"

# Ingredient Database
# https://www.notion.so/cd2598ec2530433ab675f079e9e3cb3d?v=a3e863c46ee540d1bdf4af746092910f&pvs=4
ING_DB_ID = "cd2598ec2530433ab675f079e9e3cb3d"

# Recipe Database
# https://www.notion.so/c58462890203448f9dcf50bea7c11580?v=80bcddb7fa85472aa76edf77ae9360fc&pvs=4
RECIPE_DB_ID = "c58462890203448f9dcf50bea7c11580"

# Herbs Database
# https://www.notion.so/58d3b1234b544fb2a729047083076674?v=10d0bb891c814d7d9360f3237d5291bd&pvs=4
HERB_DB_ID = "58d3b1234b544fb2a729047083076674"

# API Testing Token
# NOTION_TOKEN = "secret_AgaXegBS76SzIT8uxZh8EAqfBtswhkSRexPyrOPzdZW"

# AutoRecipe Token
NOTION_TOKEN = "secret_4YDFvqvgQF894Hgu8IrfxeLLZj7FylLkZXHOf3KJdwr"

client = NotionClient(NOTION_TOKEN)
recipe_db_obj = client.connect_database(RECIPE_DB_ID)
ing_db_obj = client.connect_database(ING_DB_ID)
herb_db_obj = client.connect_database(HERB_DB_ID)

pages = herb_db_obj.get_pages()
for page in pages:
    entry = NotionDatabaseEntry(page)
    # print(entry.properties)
    try:
        entry_name = entry.properties.get('Name').get('title')[0].get('text').get('content')
        entry_origin = entry.properties.get('Origin').get('rich_text')[0].get('text').get('content')
        print(entry_name, entry_origin)
    except Exception as e:
        print("COULD NOT", e, entry.properties)

# sample_page_id = None
#
# pages = recipe_db_obj.get_pages()
# for page in pages:
#     print("RECIPE PAGE", page)
#
#     if page.get('properties').get("Title").get('title')[0].get('text').get('content') == 'Pretzel Bread':
#         sample_page_id = page.get('id')
#         break
#
# print(sample_page_id)
#
# ing_page = ing_db_obj.get_pages(1)
# print(ing_page)
#
# db_data = {
#     "properties": {
#         "id": "jvsV",
#         "name": "Ingredients",
#         "type": "relation",
#         "relation": {
#             "database_id": ING_DB_ID,
#             "synced_property_name": "Name",
#             "synced_property_id": '0dd69a60-e4e7-4a9b-8453-db4f540b13bc'  #"%3DuuC"
#         }
#     }
# }
#
# res = recipe_db_obj.edit_page_properties(sample_page_id, db_data)
# print(res.content)
