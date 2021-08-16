import yfinance as yf
import requests
from bs4 import BeautifulSoup

class stock_financials():

    def get_stock_financials(self, ticker):
        
        self.fin_info = {}
        self.company = yf.Ticker(ticker)

        # Earnings per share part
        trailing_eps = float(self.company.info['trailingEps'])
        self.fin_info['Trailing EPS'] = trailing_eps

        # P/E Ratio
        self.fin_info['Trailing P/E'] = self.company.info['trailingPE']

        # Beta
        self.fin_info['Beta'] = self.company.info['beta']

        # Dividend
        self.fin_info['Annual Dividend Rate'] = self.company.info['trailingAnnualDividendRate']

        # Market Capitalization and Enterprise Value
        self.fin_info['Market Capitalization'] = float(self.company.info['marketCap'])
        self.fin_info['Enterprise Value'] = float(self.company.info['enterpriseValue'])


        # Extra Stats
        self.get_statistics(ticker)

        #---------- Graph Data -------------------

        # Cash
        cash = dict()
        c = self.company.balance_sheet.loc['Cash']
        for i in range(len(c)):
            cash[c.index[i].year] = c[i]
            
        self.fin_info['Cash'] = cash

        # Long Term Debt
        
        debt = dict()

        d = self.company.balance_sheet.loc['Long Term Debt']
        for i in range(len(d)):
            debt[d.index[i].year] = d[i]

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
        self.fin_info['Name'] = self.company.info['shortName']
        self.fin_info['Sector'] = self.company.info['sector']
        self.fin_info['Country'] = self.company.info['country'] 
    
        return self.fin_info
    
    
    def get_statistics(self, ticker):

        url = f"https://finance.yahoo.com/quote/{ticker}/key-statistics?p={ticker}"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

        page_source = requests.get(url, headers=headers).content
        soup = BeautifulSoup(page_source, 'html.parser')

        # ROE
        self.fin_info['Return on Equity'] = soup.find("span", text="Return on Equity").findNext('td').contents[0]
        # Revenue Growth YOY
        self.fin_info['Quarterly Revenue Growth'] = soup.find("span", text="Quarterly Revenue Growth").findNext('td').contents[0]
    








    

   


        




