# import the pre-requisite libraries
import plotly.graph_objs as go
import yfinance as yf

"""
The get_asset_pie_chart function returns the figure for the index page's pie chart
the stock_asset_dict is a dictionary passed from app.py that 
creates a dictionary of all the different sectors and the amount of 
stocks within that sector. Thus the keys are the sectors and the values are
the amount of stocks in each respective sector. All of this is possible thanks to 
Plotly. 
"""
def get_asset_pie_chart(stock_asset_dict):

    # get the names of each sector from the dictionary
    sector_list = list(stock_asset_dict.keys())

    # get the number of stocks in each resepective sector
    sector_count_list = list(stock_asset_dict.values())

    # creates a pie chart figure based on the ratio between the amount of stocks in each resepective sector
    fig = go.Figure(data=[go.Pie(labels=sector_list,
                                values=sector_count_list)])
    # styling for the figure
    fig.update_traces(hoverinfo='label+percent', marker=dict(line=dict(color='#000000', width=1)))
    
    # returns the figure
    return fig

"""
The get_fundamentals function takes a stock symbol and uses the finance API to return numerous different pieces of data
about the stock. In particular, it provides nearly all of the information necessary to create a new entry for
the stock in the database
"""
def get_fundamentals(stock_ticker):
    # create the ticker object for the stock 
    stock = yf.Ticker(stock_ticker)

    # get the stock's name
    name = stock.info["longName"]

    # get the stock's Price-Earnings Ratio
    pe = stock.info['forwardPE']

    # get the stock's daily high
    high = stock.info["dayHigh"]

    # get the stock's daily low
    low = stock.info["dayLow"]

    # get the stock's sector
    sector = stock.info["sector"]

    # compile a dictionary of all of this information
    result = {"Name" : name, "PE": pe, "dHigh" : high, "dLow" : low, "Sector" : sector, "Tickor" : stock_ticker}

    # return the dictionary
    return result

"""
The get_graph function takes in a stock's ticker and returns a figure for a graph of the stock's share price.
This function also enables numerous viewing options of the graph
"""
def get_graph(stock_ticker):

    # get the stocks name
    stock_name = yf.Ticker(stock_ticker).info["longName"]
    stock_ticker = stock_ticker.upper()
    
    # get the stock's data with an interval of 15 minutes and period of 1 day
    data = yf.download(tickers=stock_ticker, period = '1d', interval = '15m', rounding= True)
    
    # initialize and begin building the figure
    fig = go.Figure()
    
    # identify the specific information to view upon hovering along the graph
    fig.add_trace(go.Candlestick(x=data.index,open = data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name = 'market data'))
    
    # create the axes titles
    fig.update_layout(title = f'{stock_name} share price', yaxis_title = 'Stock Price (USD)')

    # enable numerous viewing options
    fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(buttons=list([
    dict(count=15, label='15m', step="minute", stepmode="backward"),
    dict(count=45, label='45m', step="minute", stepmode="backward"),
    dict(count=1, label='1h', step="hour", stepmode="backward"),
    dict(count=6, label='6h', step="hour", stepmode="backward"),
    dict(step="all")
    ])
    )
    )
    # return the figure
    return fig