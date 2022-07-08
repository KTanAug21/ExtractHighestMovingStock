from abc import ABCMeta, abstractmethod
from array import array
import csv
import requests
import os
FINNHUB_API_KEY=os.getenv("FINNHUB_API_KEY")

class SourceQuote:
    """
    Interface for getting data regarding a stock_symbol
    """
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def get_quote(self, stock_symbol:str) -> dict: 
        """
        summary:
            Returns a dictionary containing quote for a specific stock symbol
        params:
            stock_symbol:str -  specific stock symbol to get quote for
        return:
            <dict>
                current_price:int
                last_close_price:int
                percentage_change:int
        """
        raise NotImplementedError

class FinnhubQuote(SourceQuote):
    """
    Finnhub source variation of SourceQuote class
    """

    def get_quote(self, stock_symbol:str) -> dict:
        """Overrides SourceQuote.get_quote()"""
        quote_url = "https://finnhub.io/api/v1/quote?symbol={}&token={}".format(stock_symbol,FINNHUB_API_KEY)
        result    = requests.get(quote_url)
        if result.status_code == 200:
            result = result.json()
            return {
                'current_price':result['c'],
                'last_close_price':result['pc'],
                'percentage_change':result['dp']
            }
        else:
            return {
                'current_price':0,
                'last_close_price':0,
                'percentage_change':0
            }

class Stock:
    def __init__(self, stock_symbol):
        self.__stock_symbol = stock_symbol
        self.__current_price     = 0
        self.__last_close_price  = 0
        self.__percentage_change = 0

    def set_quote(self,source_quote:SourceQuote) -> None:
        """
        summary:
            Sets the current_price, last_close_price, and percentage_change attributes of the current instance
            by using the source_quote's get_quote method to request quote from source
        params:
            source_quote - class that implements the SourceQuote interface
        return:
            None    
        """
        quote_result = source_quote.get_quote(self.__stock_symbol)
        self.__current_price     = quote_result['current_price']
        self.__last_close_price  = quote_result['last_close_price']
        self.__percentage_change = quote_result['percentage_change']
        print( "{} : {}".format(self.__stock_symbol,self.__percentage_change) )

    def get_quote(self) -> dict:
        """Returns quote attributes for public viewing"""
        return {
            'stock_symbol':self.__stock_symbol,
            'percentage_change':self.__percentage_change,
            'current_price':self.__current_price,
            'last_close_price':self.__last_close_price,
        }

    def has_lower_percentage_change_than(self,other_percentage_change:int) -> bool:
        """
        summary:
            Compares whether own self.__percentage_change value is lower than other_percentage_change
        params:
            other_percentage_change:int - integer to compare to self.__percentage_change
        return:
            <bool>
        """
        if self.__percentage_change < other_percentage_change:
            return True
        else:
            return False

class StockList:
    def __init__(self,stock_symbol_list:array) -> None:
        self.__stock_symbol_list   = stock_symbol_list
        self.__most_volatile_stock = Stock("")

    def set_stock_list_values(self,source_quote:SourceQuote) -> None:
        """
        summary:
            Sets the stock quote values in the self.__stock_symbol_list
        params:
            source_quote - class that implements the SourceQuote interface
        return:
            None
        """
        for stock_symbol in self.__stock_symbol_list:
            stock = Stock(stock_symbol)
            stock.set_quote(source_quote)
            stock_data = stock.get_quote()

            if self.__most_volatile_stock.has_lower_percentage_change_than( stock_data['percentage_change'] ):
                self.__most_volatile_stock = stock

    def get_most_volatile_stock(self) -> Stock:
        """Return most volatile stock found in the list"""
        return self.__most_volatile_stock    

class CsvWriter:
    def write(self,file_name:str,header:array,row_list:array) -> None:
        """
        summary:
            Writes header and rows to a csv file
        params:
            file_name:str - name of the csv file to save, 
                          - please dont include extension
            header:array  - array of strings that will serve as the header of the csv file
            row_list:array - list of rows to write in the file
        return:
            None
        """
        with open("{}.csv".format(file_name), "w", encoding="UTF8") as f:
            writer = csv.writer(f)

            # Write the header
            writer.writerow(header)

            # Write the rows
            for row in row_list:
                writer.writerow(row)
"""
Execution code below!
"""

# NASDAQ symbols we want to include in our list
stock_symbol_list = ["AAPL","AMZN","GOOGL","META","NFLX"]

# Get quote for the stock list using the Finnhub api source
stock_list = StockList(stock_symbol_list)
stock_list.set_stock_list_values(FinnhubQuote())
most_volatile_stock = stock_list.get_most_volatile_stock()
most_volatile_quote = most_volatile_stock.get_quote()

# Print in CSV
CsvWriter().write(
    "most_volatile_stock",
    most_volatile_quote.keys(),
    [most_volatile_quote.values()]
)


