# si507_final_project

<b> Project Overview </b> <br>
This project provides information for a US zipcode or address. The information provided is average income, average housing prices, average rent prices,  and yelp resturaunt information in a flask app with plotly outputs. 

<b> Data Sources Used </b> <br>
Zillow API: API request from Zillow(https://www.zillow.com/howto/api/GetSearchResults.htm) and return the Zestimate data for homes in that zipcode

Yelp API: API request from Yelp(https://www.yelp.com/developers/documentation/v3/business_search) and return the restaurants in that zipcode + the types of restaurants + attributes

US household Income Stats: Kaggle csv file (https://www.kaggle.com/goldenoakresearch/us-household-income-stats-geo-locations#kaggle_income.csv) 

Zillow Research Housing and Rental Data: CSV file for Housing and Rental average values (https://www.zillow.com/research/data/)

US State Names and Abbreviations: CSV File used in Database (http://www.fonz.net/blog/archives/2008/04/06/csv-of-states-and-state-abbreviation)

<b> Things Needed to Run Program </b> <br>
Yelp API Key, Zillow API authentication, Plotly Key, Mapbox Key. Please refer to requirments.txt for modules needed to run program

<b> Function Definitions </b> <br>
-drop_db(): Drops any existing tables in the database <br>
-create_db(): Creates all tables populated from csv files; incomelevels, housingPrices, RentalPrices, States, and Zipcodes<br>
-yelp_api(<i>zipcode or address</i>):Calls yelp api to obtain up to 50 results of resturaunts near the zipcode and/or address <br>
-populate_yelp_table(<i> json file results</i>): Processes the json file and populates the YelpResults table in the DB <br>
-zillow_api(<i>address</i>):Calls zillow api to obtain up to zestimate, rent estimate, ect of the address <br>
-populate_zillow_table(<i> html file results</i>): Processes the html file and populates the ZillowResults table in the DB <br>
-zipcode_query(<i> zipcode, query</i>): Processes the user input to get the correct SQL statement. Query types include (home, rent, income, zillow, yelp) <br>
-process_query_yelp/zillow/income/home/rent(<i> SQL query results </i>): Processes the SQL results to give user the results in correct format<br>
-yelp/homeprices_plotly(<i>formatted SQL results output</i>): creates the different plotly graphs for each query type and returning a div tag for the flask app output <br>

<b><u> User Guide </b></u> <br>
Run the app.py file in your terminal <br>
Open the flask app <br>
Once this is opened you have the option to search by zipcode only or search by full address <br>
<b><i> Zipcode Search </b></i><br>
Enter in a US Zipcode and the information wou want <br>
Zipcode+Home: Returns boxplot of housing prices in that zipcode
Zipcode+Rent: Returns boxplot of rent prices in that zipcode
Zipcode+Yelp: Returns map of yelp resturaunts in that zipcode with hover information of name and type, piechart of price range of results, and barchart of ratings in results <br>
Zipcode+Income: Returns mean, median, and standard deviation annual income for the zipcodes
<b><i> Address Search </b></i><br>
Enter in a US Address and the information wou want <br>
Address+Home: Returns boxplot of housing prices in that zipcode
Address+Rent: Returns boxplot of rent prices in that zipcode
Address+Yelp: Returns map of yelp resturaunts in that zipcode with hover information of name and type, piechart of price range of results, and barchart of ratings in results <br>
Address+Income: Returns mean, median, and standard deviation annual income for the zipcode
Address+Zillow: Returns the avergae home price in that zipcode, the zestimate for the house, the zestimate for rent, and a link to the zillow listing
