# Import all of the necessary moduels and libraries
from flask import Flask, render_template, redirect, url_for, request, jsonify
import plotly
import json
import sqlite3
import yfinance as yf

# Importing from our helper modules
from ai_summary import stock_purchase_reasoning
from analysis_helper import get_graph, get_fundamentals, get_asset_pie_chart


# create the flask app
app = Flask(__name__)

"""
create the global variables for tracking the last stock symbol and summary. 
This is really importan in the program as it allows a recently added or dropped stock to 
inform what is rendered in the index page. PR stands for purchasing reasons and is synonymous
with the stock's summary
"""
last_stock_symbol = ''
last_PR = ''

"""
This function handles the landing page of the website and allows users to input a stock ticker into the search bar
and get a stock page that summarizes the stock's key information using Plotly, YFinance, and LangChain AI. 
"""
@app.route('/', methods=["GET", "POST"])
def get_index_page():

    # create the sqlite3 connection to begin interacting with the database!
    connection = sqlite3.connect("stock_data.db")
    cursor = connection.cursor()

    # handle the instance in which someone types in a stock ticker into the search bar
    if request.method == "POST":

        # get the stock_ticker inputted by the user
        stock_ticker = request.form.get("stock_name")

        # Google has two different tickers for nearly the same. It's a bit of an edge-case, but we're
        # only going to allow people to add the really publicly traded stock
        try:
            if stock_ticker.upper() == "GOOG":
                return redirect("/")
        except:
            return redirect("/")

        # if there's no text inputted, then simply refresh the page
        if not stock_ticker:
            return redirect("/")

        # handling the case for if someone does input something into the search bar
        else:
            # using try and except to handle the case that somone puts an invalid ticker or there's some random error
            # in the the code. This try code also handles any integers that are inputted by a user. 
            try:
                
                # upper case the stock_ticker to avoid duplicates
                stock_ticker = stock_ticker.upper()
                # save the last stock symbol to this previous one
                global last_stock_symbol
                last_stock_symbol = stock_ticker
                # get the stock graph using the get_graph function from the analysis_helper module
                fig = get_graph(stock_ticker)
                graph = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


                # get the stock fundamentals inforamtion using the analysis_helper module
                stock_fundamentals = get_fundamentals(stock_ticker)

                # initialize the last_PR
                global last_PR

                # check to see if the stock is already in the database. 
                cursor.execute("SELECT name FROM stock_data WHERE tickor = ?", (stock_ticker,))

                # fetch the single row that was queried for
                row = cursor.fetchone() 

                # if the stock isn't in the database, then you must call the AI-summary code and store the data into the database
                if row is None:

                    # set the last summary equal to what was just generated
                    PR = stock_purchase_reasoning(stock_ticker)
                    last_PR = PR
                    # add the stock data to the database using the INSERT command
                    connection.execute("INSERT INTO stock_data (name, sector, PR, PE, high, low, isAdded, tickor) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", (stock_fundamentals["Name"], stock_fundamentals["Sector"], PR, stock_fundamentals["PE"], stock_fundamentals["dHigh"], stock_fundamentals["dLow"], 0, stock_fundamentals["Tickor"]))
                
                # assemble your stock data dictionary by selecting everythin in the database that has that specific tickor
                cursor.execute("SELECT name, tickor, sector, PR, PE, high, low FROM stock_data WHERE tickor = ?", (stock_ticker,))
                
                # create the dictionary
                #get the single row for that stock's information
                row = cursor.fetchone() 
                # create a list of columns that will be used for the stock dictionary
                column_names = ['name', 'tickor', 'sector', 'PR', 'PE', 'high', 'low']
                # zip the columns and row information together
                stock_dict = dict(zip(column_names, row))

                # if the stock's summary wasn't just generated, then get the last summary based on the summary already stored in the database
                last_PR = stock_dict["PR"]

                # commit all of the sqlite3 commands
                connection.commit()
                # close out of the connection
                cursor.close()
                connection.close()
                # render the stock html code with the graph and stock_data information
                return render_template("stock.html", graph=graph, stock_data=stock_dict)
            except:
                # if an error was thrown in trying to do the above, just re-load the page
                return redirect("/")

    # handle the situation in which the index page is being rendered. 
    # for this code, we'll be assembling the pie chart and information needed to create the stock list
    else:
        # create a table of sectors and their respective stock counts from the database
        cursor.execute("SELECT DISTINCT sector, COUNT(*) as sector_count FROM stock_data WHERE isAdded = 1 GROUP BY sector;")
        
        # create a dictionary that groups all of the stock sector and the sector counts together
        stock_asset_dict = dict(cursor.fetchall())

        # get the pie chart using the helper function from the analysis_helper module
        fig = get_asset_pie_chart(stock_asset_dict)

        # assemble the pie chart that will be used in the JSON-plotly code using PLOTLY's JSON enconder
        pie_chart = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        # assembel the information for the stock list by getting the name and sector of each stock that has been added by the user
        cursor.execute("SELECT name, sector FROM stock_data WHERE isAdded = 1;")

        # create a dictionary that maps a stock to its sector
        stock_list_info = dict(cursor.fetchall())

        # render an index page that has the pie chart and stock list info 
        return render_template("index.html", pie_chart=pie_chart, stock_list_info = stock_list_info)
"""
This function handles routing that involves the specific stock page. Mainly, this functionality handles
when a user either clicks back into the main page or chooses to add or drop a stock from their portfolio.
This code uses the last stock symbol from the main route's function to determine which stock the user had just viewed,
so that when they arrive back onto the main page, they see updates to their portfolio. 

The adding and dropping feature simply involves changing the BIT values associated with each stock. This was done as opposed
to completely deleting a stock to enhance the user experience after a stock has already been looked up. 
"""
@app.route('/stock', methods=["GET", "POST"])
def get_stock_page():
    # create another instance of teh last stock symbol
    global last_stock_symbol

    # create a connection to the sqlite 3 database
    connection = sqlite3.connect("stock_data.db")
    cursor = connection.cursor()

    # check for whether a  user had made a POST request
    if request.method == "POST":

        # Access the selected option from the form data
        transaction_type = request.form.get('transactionType')
        
        # if someone had added a stock, then change the isAdded value for that stock to 1 for true
        if transaction_type == 'add':
            cursor.execute("UPDATE stock_data SET isAdded = 1 WHERE tickor = ?", (last_stock_symbol,))
        
        # if someone had added a stock, then change the isAdded value for that stock to 0 for false
        elif transaction_type == 'drop':
            cursor.execute("UPDATE stock_data SET isAdded = 0 WHERE tickor = ?", (last_stock_symbol,))
        
        # if there's no value for the transaction type, then someone chose the back button as opposed to the add/drop submission
        # this can also occur if somone chose the Selected Option as opposed to the buy or drop option in the purchase form
        else:
            # redirect users back to the home page
            return redirect("/")

        # commit all sqlite3 commands
        connection.commit()

        # close the sqlite database connection
        cursor.close()
        connection.close()

        # redirect users back to the home page
        return redirect("/")
    else:
        # if an error is thrown such that a get request is made to the stock.html page, simply return the user back to the main page
        return redirect("/")

# running the flask application when python app.py is ran in the terminal 
if __name__ == "__main__": 
    app.run(debug=False) 