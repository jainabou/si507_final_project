import sqlite3
import csv
import json
import requests
from secrets import *
from bs4 import BeautifulSoup


# Part 1: Process the income csv file

DBNAME = 'fp_database.db'
INCOMECSV = 'kaggle_input.csv'
STATESCSV='states.csv'
RENTALCSV='rental_proces-zip.csv'
HOUSINGCSV='home_sales-zip.csv'
ZIPCODECSV='zip_codes_states.csv'

# Creates a database
def drop_db():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement = '''DROP TABLE IF EXISTS States;'''
    cur.execute(statement)
    conn.commit()
    # print(cur.rowcount)

    statement = 'DROP TABLE IF EXISTS Zipcodes;'
    cur.execute(statement)
    conn.commit()

    statement = 'DROP TABLE IF EXISTS IncomeLevels;'
    cur.execute(statement)
    conn.commit()

    statement = 'DROP TABLE IF EXISTS HousingPrices;'
    cur.execute(statement)
    conn.commit()

    statement = 'DROP TABLE IF EXISTS RentalPrices;'
    cur.execute(statement)
    conn.commit()

    statement = 'DROP TABLE IF EXISTS YelpResults;'
    cur.execute(statement)
    conn.commit()

    statement = 'DROP TABLE IF EXISTS ZillowResults;'
    cur.execute(statement)
    conn.commit()

    conn.close()
    return

#drop_db()

def create_tables():
    # Connect to big10 database
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    #create state table
    statement = '''
        CREATE TABLE 'States' (
            'Id' INTEGER PRIMARY KEY,
            'Name' TEXT NOT NULL,
            'Abbr' TEXT
            );
    '''
    cur.execute(statement)

    #create zipcodes table
    statement = '''
        CREATE TABLE 'Zipcodes' (
            'Id' INTEGER PRIMARY KEY,
            'Zipcode' INTEGER NOT NULL UNIQUE,
            'state_id' INTEGER,
            'lat' INTEGER,
            'lon' INTEGER,
            FOREIGN KEY(state_id) REFERENCES States(Id)
            );
    '''
    cur.execute(statement)

    #create IncomeLevels table
    statement = '''
        CREATE TABLE 'IncomeLevels' (
            'Id' INTEGER PRIMARY KEY,
            'zipcode_id' INTEGER,
            'mean_income' INTEGER,
            'median_income' INTEGER,
            'std_income' INTEGER,
            FOREIGN KEY(zipcode_id) REFERENCES Zipcodes(Id)
            );
    '''
    cur.execute(statement)

    #create HousingPrices table
    statement = '''
        CREATE TABLE 'HousingPrices' (
            'Id' INTEGER PRIMARY KEY,
            'zipcode_id' INTEGER,
            '2017_avg' INTEGER,
            '2017_std' INTEGER,
            '2018_avg' INTEGER,
            '2018_std' INTEGER,
            FOREIGN KEY(zipcode_id) REFERENCES Zipcodes(Id)
            );
    '''
    cur.execute(statement)

    #create RentalPrices table
    statement = '''
        CREATE TABLE 'RentalPrices' (
            'Id' INTEGER PRIMARY KEY,
            'zipcode_id' INTEGER,
            '2017_avg' INTEGER,
            '2017_std' INTEGER,
            '2018_avg' INTEGER,
            '2018_std' INTEGER,
            FOREIGN KEY(zipcode_id) REFERENCES Zipcodes(Id)
            );
    '''
    cur.execute(statement)

    #create yelp table
    statement = '''
        CREATE TABLE 'YelpResults' (
            'Id' INTEGER PRIMARY KEY,
            'zipcode_id' INTEGER,
            'buisness_name' TEXT,
            'lat' INTEGER,
            'lon' INTEGER,
            'buisness_price' TEXT,
            'rating' INTEGER,
            'site_url' TEXT,
            FOREIGN KEY(zipcode_id) REFERENCES Zipcodes(Id)
            );
    '''
    cur.execute(statement)

    #create zillow table
    statement = '''
        CREATE TABLE 'ZillowResults' (
            'Id' INTEGER PRIMARY KEY,
            'zipcode_id' INTEGER,
            'ze_home_value' INTEGER,
            'ze_rent_value' INTEGER,
            'lat' INTEGER,
            'lon' INTEGER,
            'ze_home_high_value' INTEGER,
            'ze_home_low_value' INTEGER,
            'ze_rent_high_value' INTEGER,
            'ze_rent_low_value' INTEGER,
            'site_url' TEXT,
            FOREIGN KEY(zipcode_id) REFERENCES Zipcodes(Id)
            );
    '''
    cur.execute(statement)

    #populate states into database
    with open(STATESCSV) as csvDataFile:
        csvReader=csv.reader(csvDataFile)
        next(csvReader)
        for row in csvReader:
            statename=row[0]
            stateabbr=row[1]

            insertion=(None,statename, stateabbr)
            # print(insertion)
            statement ='INSERT OR REPLACE INTO "States" (Id,Name,Abbr)'
            statement +='VALUES (?, ?, ?)'
            cur.execute(statement, insertion)


    #populate states into database
    with open(ZIPCODECSV) as csvDataFile:
        csvReader=csv.reader(csvDataFile)
        next(csvReader)
        for row in csvReader:
            zipcode=row[0]
            lat=row[1]
            lon=row[2]
            stateabbr=row[4]
            state_id=None

            statement='SELECT Id from States WHERE Abbr= "'+str(stateabbr)+'" '
            #print(statement)
            cur.execute(statement)
            i=cur.fetchone()
            if i is not None:
                state_id=i[0]

            insertion=(None,zipcode, state_id, lat, lon)
            # print(insertion)
            statement ='INSERT INTO "Zipcodes" '
            statement +='VALUES (?, ?, ?, ?, ?)'
            cur.execute(statement, insertion)

    #populate income into database
    with open(INCOMECSV) as csvDataFile:
        csvReader=csv.reader(csvDataFile)
        next(csvReader)
        for row in csvReader:
            zipcode_id=None
            zipcode=row[9]
            mean_income=row[15]
            median_income=row[16]
            std_income=row[17]
            #get the state id
            #print(statename)
            statement='SELECT Id from Zipcodes WHERE Zipcode= "'+str(zipcode)+'" '
            #print(statement)
            cur.execute(statement)
            i=cur.fetchone()
            if i is not None:
                zipcode_id=i[0]

            insertion=(None,zipcode_id, mean_income, median_income, std_income)
            statement ='INSERT INTO "IncomeLevels" '
            statement +='VALUES (?, ?, ?, ?, ?)'
            cur.execute(statement, insertion)

    #populate RentalPrices into database
    with open(RENTALCSV) as csvDataFile:
        csvReader=csv.reader(csvDataFile)
        next(csvReader)
        for row in csvReader:
            zipcode_id=None
            zipcode=row[0]
            avg2017=row[6]
            std2017=row[7]
            avg2018=row[8]
            std2018=row[9]
            #get the state id
            #print(statename)
            statement='SELECT Id from Zipcodes WHERE Zipcode= "'+str(zipcode)+'" '
            #print(statement)
            cur.execute(statement)
            i=cur.fetchone()
            if i is not None:
                zipcode_id=i[0]

            insertion=(None,zipcode_id, avg2017, std2017, avg2018, std2018)
            statement ='INSERT INTO "RentalPrices" '
            statement +='VALUES (?, ?, ?, ?, ?, ?)'
            cur.execute(statement, insertion)

    #populate RentalPrices into database
    with open(HOUSINGCSV) as csvDataFile:
        csvReader=csv.reader(csvDataFile)
        next(csvReader)
        for row in csvReader:
            zipcode_id=None
            zipcode=row[0]
            avg2017=row[3]
            std2017=row[4]
            avg2018=row[5]
            std2018=row[6]
            #get the state id
            #print(statename)
            statement='SELECT Id from Zipcodes WHERE Zipcode= "'+str(zipcode)+'" '
            #print(statement)
            cur.execute(statement)
            i=cur.fetchone()
            if i is not None:
                zipcode_id=i[0]

            insertion=(None,zipcode_id, avg2017, std2017, avg2018, std2018)
            statement ='INSERT INTO "HousingPrices" '
            statement +='VALUES (?, ?, ?, ?, ?, ?)'
            cur.execute(statement, insertion)

    conn.commit()

    conn.close()
    return

#create_tables()

#YelpAPI
CACHE_YNAME = 'yelp_cache.json'
BASEURL_YELP='https://api.yelp.com/v3/businesses/search'
CACHE_ZNAME = 'zillow_cache.json'
BASEURL_ZILLOW='http://www.zillow.com/webservice/GetSearchResults.htm?'

def cache_memory_yelp():
    try:
        cache_file = open(CACHE_YNAME, 'r')
        cache_contents = cache_file.read()
        CACHE_DICTION = json.loads(cache_contents)
        cache_file.close()
    except:
        CACHE_DICTION={}
    return CACHE_DICTION

def cache_memory_zillow():
    try:
        cache_file = open(CACHE_ZNAME, 'r')
        cache_contents = cache_file.read()
        CACHE_DICTION = json.loads(cache_contents)
        cache_file.close()
    except:
        CACHE_DICTION={}
    return CACHE_DICTION

def params_unique_combination(baseurl, params):#combine URL and parameter for
    alphabetized_keys = params.keys()
    res = []
    for k in alphabetized_keys:
        res.append("{}={}".format(k, params[k]))
    URL=baseurl + "&".join(res)
    print(URL)
    return URL

def make_request_using_cache_yelp(baseurl, params):
    headers={'Authorization': 'bearer %s'%YELP_KEY}
    unique_ident = params_unique_combination(baseurl, params)
    #print(unique_ident)
    CACHE_DICTION=cache_memory_yelp()

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
            print("Getting cached data...")
            return CACHE_DICTION[unique_ident]
    else:
        #if not, run the API request
        print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(url=baseurl, params=params, headers=headers)
        print(resp.text)
        CACHE_DICTION[unique_ident] = json.loads(resp.text)#convery request into txt, then load into json file
        dumped_json_cache = json.dumps(CACHE_DICTION, indent=1) #dump dictionary into string
        fw = open(CACHE_YNAME,"w") #wirte string into file
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        locations=CACHE_DICTION[unique_ident]
        return locations

def make_request_using_cache_zillow(baseurl, params):
    unique_ident = params_unique_combination(baseurl, params)
    #print(unique_ident)
    CACHE_DICTION=cache_memory_zillow()

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
            print("Getting cached data...")
            return CACHE_DICTION[unique_ident]
    else:
        #if not, run the API request
        print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(baseurl, params)
        res_soup=BeautifulSoup(resp.text, 'html.parser')
        CACHE_DICTION[unique_ident] = str(res_soup)

        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_ZNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]

def yelp_api_zip(zipcode):
    #obtian the lon and lat for zipcode
    lat=None
    lon=None
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement='SELECT lat,lon from Zipcodes WHERE Zipcode= "'+str(zipcode)+'" '
    cur.execute(statement)
    results=cur.fetchall()
    for i in results:
        lat=i[0]
        lon=i[1]
    conn.close()
    #print(lat)
    #print(lon)
    if lat and lon is not None:
        baseurl=BASEURL_YELP
        params_diction = {}
        params_diction["term"] = 'restaurants'
        params_diction["latitude"] = lat
        params_diction["longitude"] = lon
        return make_request_using_cache_yelp(baseurl, params_diction)
    else:
        err_statement='Sorry, no location was found for this zipcode. Please try another query.'
        return print(err_statement)

# yelp_api_zip(48188)

def yelp_api_address(location):
    #obtian the lon and lat for zipcode
    location_str=str(location)

    baseurl=BASEURL_YELP
    params_diction = {}
    params_diction["term"] = 'restaurants'
    params_diction["location"] = location_str
    return make_request_using_cache_yelp(baseurl, params_diction)

def populate_yelp_table(json):

    buisness_list=json['businesses']
    # Connect to big10 database
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    #create state table
    for i in buisness_list:
        zipcode_id=None
        price=None
        name=i['name']
        url=i['url']
        rating=i['rating']
        lat=i['coordinates']['latitude']
        lon=i['coordinates']['longitude']
        if 'price' in i.keys():
            price=i['price']
        zipcode=i['location']['zip_code']

        statement='SELECT Id from Zipcodes WHERE Zipcode= "'+str(zipcode)+'" '
        #print(statement)
        cur.execute(statement)
        i=cur.fetchone()
        if i is not None:
            zipcode_id=i[0]
        print(zipcode_id)
        insertion=(None,zipcode_id, name, lat, lon, price,rating,url)
        # print(insertion)
        statement ='INSERT INTO "YelpResults" '
        statement +='VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
        cur.execute(statement, insertion)
    conn.commit()

    conn.close()
    return

populate_yelp_table(yelp_api_address('47568 pembroke dr canton mi '))


def zillow_api(location, zip):
    location_str=str(location)
    zipcode=str(zip)
    baseurl=BASEURL_ZILLOW
    params_diction = {}
    params_diction["address"] = location_str
    params_diction["citystatezip"] = zipcode
    params_diction["rentzestimate"] = 'true'
    #params_diction["locationbias=circle:"]=radius
    params_diction["zws-id"]=ZWSID
    return make_request_using_cache_zillow(baseurl, params_diction)

def populate_zillow_table(html_requests):
    results=BeautifulSoup(html_requests,'html.parser')
    zipcode=results.find('zipcode').text
    lat=results.find('latitude').text
    lon=results.find('longitude').text
    zest_home=results.find('zestimate').find('amount').text
    print(zest_home)
    zest_home_range=results.find_all('zestimate')
    for i in zest_home_range:
        high_home=i.find('high').text
        print(high_home)
        low_home=i.find('low').text
        print(low_home)

    zest_rent=results.find('rentzestimate').find('amount').text
    print(zest_rent)
    zest_rent_range=results.find_all('rentzestimate')
    for i in zest_rent_range:
        high_rent=i.find('high').text
        print(high_rent)
        low_rent=i.find('low').text
        print(low_rent)
    url=results.find('links').find('homedetails').text
    print(url)

    #get zipcode id for entry
    # Connect to big10 database
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement='SELECT Id from Zipcodes WHERE Zipcode= "'+str(zipcode)+'" '
    #print(statement)
    cur.execute(statement)
    i=cur.fetchone()
    if i is not None:
        zipcode_id=i[0]
    print(zipcode_id)
    insertion=(None,zipcode_id, zest_home,zest_rent, lat, lon,high_home,low_home,high_rent,low_rent,url)
    # print(insertion)
    statement ='INSERT INTO "ZillowResults" '
    statement +='VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    cur.execute(statement, insertion)
    conn.commit()
    conn.close()

    return

populate_zillow_table(zillow_api('3810 saddlebrook ct upper marlboro md',20772))
