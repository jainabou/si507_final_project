import unittest
from data_processing import *

class TestDataBase(unittest.TestCase):

    drop_db()
    create_tables()

    def testZipcodes(self):
        # drop_db()
        # create_tables()
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT Zipcode FROM Zipcodes'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn((48188,), result_list)
        self.assertEqual(len(result_list), 42741)


        conn.close()

    def testStates(self):
        # drop_db()
        # create_tables()
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT Name FROM States'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Alabama',), result_list)
        self.assertEqual(len(result_list), 51)


        conn.close()

    def testHousingLevels(self):
        # drop_db()
        # create_tables()
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT [2017_avg] FROM HousingPrices as h JOIN Zipcodes as z ON z.Id=h.zipcode_id WHERE z.Zipcode=48188'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn((281516.6667,), result_list)
        self.assertEqual(len(result_list), 1)
        conn.close()

    def testIncomeLevels(self):
        # drop_db()
        # create_tables()
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT [mean_income] FROM IncomeLevels as h JOIN Zipcodes as z ON z.Id=h.zipcode_id WHERE z.Zipcode=48188'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn((90008,), result_list)
        self.assertEqual(len(result_list), 2)
        conn.close()

    def testYelpresults(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        populate_yelp_table(yelp_api_zip(48188))

        sql = 'SELECT [buisness_name] FROM YelpResults as h JOIN Zipcodes as z ON z.Id=h.zipcode_id WHERE z.Zipcode=48188'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(("Famous Hamburger - Canton",), result_list)
        self.assertEqual(len(result_list), 3)
        conn.close()

    def testZillowresults(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        populate_zillow_table(zillow_api('47568 pembroke dr canton mi',48188))

        sql = 'SELECT [ze_home_value] FROM ZillowResults as h JOIN Zipcodes as z ON z.Id=h.zipcode_id WHERE z.Zipcode=48188'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn((176947,), result_list)
        self.assertEqual(len(result_list), 1)
        conn.close()

    def testZipcoderesults_zillow(self):

        results=zipcode_query(48188,'zillow')


        #print(results)
        self.assertIn("Michigan", results[0][0])
        self.assertEqual(len(results), 1)

    def testZipcoderesults_yelp(self):

        results=zipcode_query(48188,'yelp')


        #print(results)
        self.assertIn("Burgers", results[0][5])
        self.assertEqual(len(results), 3)

    def testZipcoderesults_home(self):

        results=zipcode_query(48188,'home')


        #print(results)
        self.assertIn("112706.0", str(results[0][4]))
        self.assertEqual(len(results), 1)

    def testZipcoderesults_rent(self):

        results=zipcode_query(48188,'rent')


        # print(results)
        self.assertIn("1676.25", str(results[0][7]))
        self.assertEqual(len(results), 1)

unittest.main()
