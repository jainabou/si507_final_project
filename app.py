from flask import Flask, render_template, request, redirect
import data_processing

app = Flask(__name__)

# print(data_processing.avg_homeprice)

zipcode=None
query=None
address=None
@app.route('/')
def index():
    return '''
        <h1>Zipcode Information Finder!</h1>
        <ul>
            <li><a href="/homesearch"> Search ZipCode </a></li>
            <li><a href="/addressearch"> Search Address </a></li>
        </ul>
    '''

@app.route('/addressearch', methods=['GET', 'POST'])
def aball():

    return render_template("address_page.html")

@app.route('/homesearch', methods=['GET', 'POST'])
def fball():

    return render_template("home_page.html")
    #return redirect("/")


@app.route("/postentryzip", methods=["POST"])
def postentry():
    #print(request.form)
    global zipcode
    global query
    try:
        zipcode = request.form["name"]
        query=request.form["value"]
        if query=='home':
            data_processing.process_query_income(data_processing.zipcode_query(zipcode,'home'))
            return redirect('/homeplotly')
        if query =='rent':
            data_processing.process_query_income(data_processing.zipcode_query(zipcode,'rent'))
            return redirect('/homeplotly')
        if query=='yelp':
            data_processing.populate_yelp_table(data_processing.yelp_api_zip(zipcode))
            data_processing.process_query_yelp(data_processing.zipcode_query(zipcode,'yelp'))
            return redirect('/yelpplotly')
        if query=='income':

            return redirect('/incomedata')
        if query=='zillow':

            return redirect('/zillowinfo')
                # #yelp_plotly()
    #    message = request.form["message"]
        #rint(query)
        return redirect("/")
    except:
        return redirect("/helppage")

@app.route('/helppage', methods=['GET', 'POST'])
def helppage():

    return render_template("error_page.html")

@app.route("/postentryzillow", methods=["POST"])
def postentryzillow():
    #print(request.form)
    global zipcode
    global query
    global address
    try:
        zipcode = request.form["name"]
        query=request.form["value"]
        street=request.form["address"]
        citystate=request.form["citystate"]
        address=str(street)+' '+str(citystate)
        if query=='home':
            data_processing.process_query_income(data_processing.zipcode_query(zipcode,'home'))
            return redirect('/homeplotly')
        if query =='rent':
            data_processing.process_query_income(data_processing.zipcode_query(zipcode,'rent'))
            return redirect('/homeplotly')
        if query=='yelp':
            data_processing.populate_yelp_table(data_processing.yelp_api_zip(zipcode))
            data_processing.process_query_yelp(data_processing.zipcode_query(zipcode,'yelp'))
            return redirect('/yelpplotly')
        if query=='income':

            return redirect('/incomedata')
        if query=='zillow':
            data_processing.populate_zillow_table(data_processing.zillow_api(address,zipcode))
            return redirect('/zillowinfo')
                # #yelp_plotly()
    #    message = request.form["message"]
        #rint(query)
        return redirect("/")
    except:
        return redirect("/helppage")

@app.route("/incomedata")
def incomedata():
    g=data_processing.process_query_income(data_processing.zipcode_query(zipcode,'rent'))
    mean=g[0]
    std=g[1]
    median=g[2]
    return render_template("incomedata.html", mean=mean,  std=std, median=median, zipcode=zipcode)

@app.route("/zillowinfo")
def zillowdata():
    g=data_processing.process_query_zillow(data_processing.zipcode_query(zipcode,'zillow'))
    mean=g[0]
    home_2018=g[1]
    rent_2018=g[2]
    ze_home=g[3]
    ze_rent=g[4]
    url=g[5]
    return render_template("zillow_page.html", mean=mean,  home_2018=home_2018, rent_2018=rent_2018, zipcode=zipcode, address=address,ze_home=ze_home, ze_rent=ze_rent, url=url)

@app.route('/yelpplotly')
def yelp_plot():
    plot=data_processing.yelp_plotly()
    plot2=data_processing.yelp_pie_plotly(data_processing.yelp_count_query(zipcode))
    pie_chart=plot2[0]
    bar_chart=plot2[1]
    return render_template("yelp_page.html", seasons=plot,pie_chart=pie_chart,bar_chart=bar_chart, zipcode=zipcode, query=query)

@app.route('/homeplotly')
def home_price():
    plot=data_processing.homeprices_plotly()
    return render_template("home_price.html", seasons=plot, zipcode=zipcode, query=query)

@app.route("/back", methods=["POST"])
def deleteentry():
    #id = request.form["id"]
    #model1.delete_entry(id)
    return redirect("/")

if __name__ == '__main__':
    data_processing.drop_db()
    data_processing.create_tables()

    app.run(debug=True)
