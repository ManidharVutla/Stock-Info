import yfinance as yf
import requests
from bs4 import BeautifulSoup

class stock_financials():

    def get_stock_financials(self, ticker):
        
        self.fin_info = {}
        self.company = yf.Ticker(ticker)

        # Earnings per share part
        trailing_eps = float(self.fetch_data('trailingEps'))
        self.fin_info['Trailing EPS'] = trailing_eps

        # P/E Ratio
        self.fin_info['Trailing P/E'] = self.fetch_data('trailingPE')

        # Beta
        self.fin_info['Beta'] = self.fetch_data('beta')

        # Dividend
        self.fin_info['Annual Dividend Rate'] = self.fetch_data('trailingAnnualDividendRate')

        # Market Capitalization and Enterprise Value
        self.fin_info['Market Capitalization'] = float(self.fetch_data('marketCap'))
        self.fin_info['Enterprise Value'] = float(self.fetch_data('enterpriseValue'))


        # Extra Stats
        self.get_statistics(ticker)

        #---------- Graph Data -------------------

  
        # Cash
        c = self.fetch_data('Cash') 
        cash = self.get_cash_or_debt_history(c)  
            
        self.fin_info['Cash'] = cash

        # Long Term Debt
        
        d = self.fetch_data('Long Term Debt') 
        debt = self.get_cash_or_debt_history(d)

        self.fin_info['Long Term Debt'] = debt

        # Major Stock Holders
        holders = dict()

        h = self.company.major_holders

        for i in range(len(h[0])-2):
            holders[h[1][i]] = h[0][i]
        
        self.fin_info['major stock holders'] = holders

        # Recommendations
        recommendations = dict()

        b = self.company.recommendations
        n = len(b)
        for i in range(n-6, n-1):
            recommendations[b.iloc[i]['Firm']] = b.iloc[i]['To Grade']
        
        self.fin_info['recent_recommendations'] = recommendations

        # Adding Company Info
        self.fin_info['Name'] = self.fetch_data('shortName') 
        self.fin_info['Sector'] = self.fetch_data('sector') 
        self.fin_info['Country'] = self.fetch_data('country') 
    
        return self.fin_info
    
    def fetch_data(self, metric):
        try:
            if metric == 'Cash' or metric == 'Long Term Debt':
                metric_data = self.company.balance_sheet.loc[metric]
            else:
                metric_data = self.company.info[metric]
        except KeyError as error:
            metric_data = 'Fetching Failed'
        return metric_data
    
    def get_cash_or_debt_history(self, data_dump):

        recent_figures = dict()
        if type(data_dump) != str:
            for i in range(len(data_dump)):
                recent_figures[data_dump.index[i].year] = data_dump[i]
        return recent_figures
            

    def get_statistics(self, ticker):

        url = f"https://finance.yahoo.com/quote/{ticker}/key-statistics?p={ticker}"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

        page_source = requests.get(url, headers=headers).content
        soup = BeautifulSoup(page_source, 'html.parser')

        # ROE
        self.fin_info['Return on Equity'] = soup.find("span", text="Return on Equity").findNext('td').contents[0]
        # Revenue Growth YOY
        self.fin_info['Quarterly Revenue Growth'] = soup.find("span", text="Quarterly Revenue Growth").findNext('td').contents[0]
    








    

   


        




