import json

import pymongo
import qwikidata as qwikidata
import requests
from util.common import load_from_mongo
from string import digits
import pycountry
from pymongo import UpdateOne
from qwikidata.sparql import return_sparql_query_results
from wikipedia_scraper import settings
import re


def get_city_opendata(city, country):
    link = 'https://public.opendatasoft.com/api/records/1.0/search/?dataset=worldcitiespop&q={}&sort=population&facet=country&refine.country={}'.format(
        city, country)
    print(link)
    res = requests.get(link)
    dct = json.loads(res.content)
    if 'population' in dct['records'][0]['fields']:
        out = dct['records'][0]['fields']['population']
    else:
        out = 0

    return out


def get_city_wikidata(city, country):
    query = """
    SELECT ?city ?cityLabel ?country ?countryLabel ?population
    WHERE
    {
      ?city rdfs:label '%s'@en.
      ?city wdt:P1082 ?population.
      ?city wdt:P17 ?country.
      ?city rdfs:label ?cityLabel.
      ?country rdfs:label ?countryLabel.
      FILTER(LANG(?cityLabel) = "en").
      FILTER(LANG(?countryLabel) = "en").
      FILTER(CONTAINS(?countryLabel, "%s")).
    }
    """ % (city, country)

    res = return_sparql_query_results(query)
    if len(res['results']['bindings']) > 0:
        out = res['results']['bindings'][0]
        return out['population']['value']

    return -1


def fix_city_name(city):
    m = re.search(r"\d+", city)
    if m is not None:
        return city[m.end():]

    return city


museum_data = load_from_mongo()

remove_digits = str.maketrans('', '', digits)

mongo_bulk = []

museum_data = museum_data[0:10]

for museum in museum_data:
    if not 'Location' in museum:
        continue

    if len(museum['Location'].split(",")) < 2:
        print("Invalid location: {}".format(museum['Location']))
        continue

    city, country = museum['Location'].split(",")[-2:]
    city = fix_city_name(city).strip().lower().capitalize()
    country = country.strip().capitalize()
    pop_data = get_city_wikidata(city, country)
    # museum['population'] = pop_data
    mongo_bulk.append(UpdateOne({'_id': museum['_id']}, {'$set': {'population': pop_data}}))

connection = pymongo.MongoClient(
    settings.MONGODB_SERVER,
    settings.MONGODB_PORT
)
db = connection[settings.MONGODB_DB]
collection = db[settings.MONGODB_COLLECTION]

collection.bulk_write(mongo_bulk)

