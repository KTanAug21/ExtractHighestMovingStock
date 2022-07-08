## ExtractHighestMovingStock

Script that creates a csv file containing information about the highest moving stock between Apple, Amazon, Netflix, Facebook, Google companies.
Retrieves stock data from https://finnhub.io/.

Exports highest stock to a csv file as a result.

## Setup
1. Register an account in https://finnhub.io/register and get your api key from the dashboard
2. Add the api key as an environment variable:
FINNHUB_API_KEY="<key_here>"


## Parts of the logic
1. Data retrieval from source
2. Stock record containing relevant attributes
3. Stock List that keeps track of the most volatile Stock
4. Writing of information to a csv file

# Relevant Classes derived from parts above:
1. SourceQuote 
- handles the retrieval of actual stock data from a source
- created as a class with the role of an interface,
- Currently implemented by class FinnhubQoute
- creating this as an interface allows adding of new sources in the future without having to make revision on the existing code that calls instances of this class, follows open-close principle

2. Stock 
- receives the stock symbol, and SourceQuote instance
- responsible for calling SourceQuote to get quote details for the stock symbol
- records actual stock symbol quotation
- responsible for determining whether its percentage_change is lower than a given input

3. StockList
- receives list of stock symbols, and SourceQuote instance
- creates a list of stock symbols and their quotes values using the Stock
- keeps track of most_volatile_stock

4. CsvWriter
- writes the most_volatile_stock details into a csv file


