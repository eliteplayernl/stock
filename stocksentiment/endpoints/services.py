'''
Created on May 23, 2013

@author: Ashish
'''
from google.appengine.ext import endpoints
from protorpc import messages
from protorpc import remote
from persistence.structure import StockSymbol
from persistence.StockSymbols import StockSymbols

class Sentiment(messages.Message):
    category = messages.StringField(1)
    keyword= messages.StringField(2)
    
class StockSymbolMessage(messages.Message):
    symbol = messages.StringField(1)
    companyName = messages.StringField(2)
    exchange = messages.StringField(3)
    
class StockSymbolList(messages.Message):
    items = messages.MessageField(StockSymbolMessage, 1, repeated=True)
    
@endpoints.api(name='sentiment', version='v1', description='Sentiment API')
class SentimentAPI(remote.Service):
    @endpoints.method(request_message=Sentiment,response_message=Sentiment, name='insert', path='add', http_method='POST')
    def addSentiment(self,request):
        return request

@endpoints.api(name='symbols', version='v1', description='Stock Symbols API')
class GetSymbolsAPI(remote.Service):
    @endpoints.method(response_message=StockSymbolList, name='get', path='symbols', http_method='GET')
    def getSymbols(self, request):
        symbols = []
        for sym in StockSymbol.query():
            symbols.append(StockSymbolMessage(symbol=sym.symbol, companyName=sym.companyName, exchange=sym.exchange))
        
        return StockSymbolList(items=symbols)
    
    @endpoints.method(name='add', path='symbols', http_method='POST')
    def addSymbols(self, request):
        stock = StockSymbols()
        stock.store()
        
        return request

    
application = endpoints.api_server([GetSymbolsAPI])

