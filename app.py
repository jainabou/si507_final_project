from flask import Flask, render_template, request, redirect
import data_processing

app = Flask(__name__)

# print(data_processing.avg_homeprice)

zipcode=None
query=None

@app.route('/')
def index():
    return '''
        <h1>Zipcode Information Finder!</h1>
        <ul>
            <li><a href="/homesearch"> Search ZipCode </a></li>
        </ul>
    '''

@app.route('/homesearch', methods=['GET', 'POST'])
def fball():
    # if request.method == 'POST':
    #     zipcode = request.form['zipcode']
    #     #sortorder = request.form['sortorder']
    #     #seasons = model.get_football_seasons(sortby, sortorder)
    #     print(zipcode)

    return render_template("home_page.html")
    #return redirect("/")


@app.route("/postentryzip", methods=["POST"])
def postentry():
    #print(request.form)
    global zipcode
    global query
    zipcode = request.form["name"]
    query=request.form["value"]
    if query=='home':
        data_processing.process_query_income(data_processing.zipcode_query(zipcode,'home'))
        return redirect('/homeplotly')
    if query =='rent':
        data_processing.process_query_income(data_processing.zipcode_query(zipcode,'rent'))
        return redirect('/homeplotly')
    if query=='yelp':
        data_processing.yelp_api_zip(zipcode)
        data_processing.process_query_yelp(data_processing.zipcode_query(zipcode,'yelp'))
        return redirect('/yelpplotly')
            # #yelp_plotly()
#    message = request.form["message"]
    #rint(query)
    return redirect("/")

@app.route('/yelpplotly')
def yelp_plot():
    plot=data_processing.yelp_plotly()
    return render_template("yelp_page.html", seasons=plot, zipcode=zipcode, query=query)

@app.route('/homeplotly')
def home_price():
    plot=data_processing.homeprices_plotly()
    return render_template("home_price.html", seasons=plot, zipcode=zipcode, query=query)

@app.route("/back", methods=["POST"])
def deleteentry():
    #id = request.form["id"]
    #model1.delete_entry(id)
    return redirect("/homesearch")

if __name__ == '__main__':
    data_processing.drop_db()
    data_processing.create_tables()
    #data_processing.process_query_income(data_processing.zipcode_query(20772,'home'))
#    homeprices_plotly()
#    print(data_processing.avg_homeprice)
    app.run(debug=True)
