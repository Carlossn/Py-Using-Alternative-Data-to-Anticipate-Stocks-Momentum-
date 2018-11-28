from scrapy import Spider
from scrapy.selector import Selector
from mojo.items import MovieItem
import scrapy # you need this to call scrapy.Request
from datetime import datetime
#http://www.boxofficemojo.com/studio/chart/?view=parent&view2=release&yr=2016&timeframe=yty&sort=&order=&studio=buenavista.htm

class MojoSpider(Spider):
    name = "mojo_spider"
    allowed_urls = ['http://www.boxofficemojo.com/']
    
    dict1 = {'Disney':'buenavista','Time Warner':'wip', 'Fox':'foxsearchlight','Sony': 'sonyrepertory','Lionsgate':'lionsgate','Viacom (Paramount)':'paramountclassics','Comcast':'universal','Weinstein Co':'weinsteincompany'}
    Parent = dict1['Weinstein Co'] # choose   
    start = 2010
    end = 2016
    period = range(start,end+1,1)
    period
    base1 = "http://www.boxofficemojo.com/studio/chart/?yr="
    base2 = "&view=parent&view2=calendar&timeframe=yty&studio="
    tail = ".htm&sort=open&order=DESC&p=.htm"

    start_urls = [base1+str(i)+base2+Parent+tail for i in period] 
    

    def parse(self, response):
        rows = response.xpath('//*[@id="body"]/table[4]//tr').extract()  
        link_l = []

        for row in rows[1:]: # rows[0] are only the columns names 
            l = Selector(text=row).xpath('//td[3]/b/font/a/@href').extract() # use empty list [] as condition to reject right below:
            if l!=[]:
                link_l.append('http://www.boxofficemojo.com' + l[0].encode('utf-8', 'ignore')) # this creates the list of movies links for a specific year/top studio. The conditional eliminates empty objects

        for link in link_l: # for every movie link in our list, we want to open a door to scrap:
            yield scrapy.Request(link, callback=self.movie_details) # you are creating a new request for link that creates a new response object.


    def movie_details(self, response): # it called  by the line above and works around a new response object Q2: Why in termninal typing scrapy.Request(url) doesn't generate new url?

            tab1 = response.xpath('//*[@id="body"]/table[1]').extract()
            
            
            Name = str(Selector(text=tab1[0]).xpath('//tr/td[2]/font/b/text()').extract()[0].encode('utf-8', 'ignore'))   
            Distrib = Selector(text=tab1[0]).xpath('//tr[2]/td[1]/b/a/text()').extract()[0].encode('utf-8', 'ignore')
            Genre = Selector(text=tab1[0]).xpath('//tr[3]/td[1]/b/text()').extract()[0].encode('utf-8', 'ignore')
            
            try: Opening = float(Selector(text=tab1[0]).xpath('//td[1]//tr/td[1]/div[2]/div[2]/table[1]//tr[1]/td[2]/text()').extract()[0].encode('utf-8', 'ignore').replace('\xc2\xa0$','').replace(',',''))/1000000
            except: Opening = 'N/A'
            
            try: Domestic = round(float(Selector(text=tab1[0]).xpath('//tr[1]/td[2]/b/text()').extract()[0].encode('utf-8', 'ignore').replace(',','').replace('$',''))/1000000,3)
            except: Domestic = 'N/A'
            
            try: Total = round(float(Selector(text=tab1[0]).xpath('//tr//tr[4]/td[2]/b/text()').extract()[1].encode('utf-8', 'ignore').replace(',','').replace('$',''))/1000000,3)
            except: Total = 'N/A'

            try: Overseas = round(float(Selector(text=tab1[0]).xpath('//tr/td[1]/div[1]/div[2]//tr[2]/td[2]/text()').extract()[0].encode('utf-8', 'ignore').replace('\xc2\xa0$','').replace(',',''))/1000000,3)
            except: Overseas = 'N/A'
            
            try: self.Budget = float(Selector(text=tab1[0]).xpath('//tr[4]/td[2]/b/text()').extract()[0].encode('utf-8', 'ignore').replace('$','').replace(' million',''))
            except: 
                try: 
                     yield scrapy.Request('http://www.the-numbers.com/movie/budgets/all', callback=self.budget_backup)
                    

                except: self.Budget= None # you need none here to control for documentary(below)
        
            self.Budget = min(self.Budget, 5) if Genre == 'Documentary'else self.Budget # IMDb estimates 5 Mill by default for documentaries without actual data    
                
            # Mkting Expenses Estimates: 0.5% Budget if Budget>40 Mill USD, 100% Production Budget if it is >5 and <40 Mill USD and 150% for 1-5 Mill USD Budgets.
            try: Mkting = [self.Budget*1.5 if self.Budget<5 else self.Budget*1 if self.Budget<40 else self.Budget*0.5][0] 
            except: Mkting = 'N/A'
            
            try:
                dat =  Selector(text=tab1[0]).xpath('//tr[2]/td[2]/b/nobr/a/@href').extract()[0].encode('utf-8','ignore').replace('&p=.htm','')
                Date = datetime.strptime(dat[len(dat)-10:len(dat)] , '%Y-%m-%d').date() # date object
            except: Date = 'N/A' 

            try: Year = Date.year 
            except: Year = 'N/A' 

            # Parent Revennue Estimates: 55% Boc Office if Budget<5 Mill USD, 60% Box Office for Budget between 5-40 Mill USD and 65% for >40 Mill USD.       
            try: ParentRev = round([Total*0.55 if self.Budget<5 else Total*0.6 if self.Budget<40 else Total*0.65][0],3)
            except: ParentRev = 'N/A'

            try: GProfit = round(ParentRev - self.Budget,3)
            except: GProfit = 'N/A'
            
            try: NProfit = round(GProfit - Mkting,3)
            except: NProfit = 'N/A'

            try: ROC = 100* round(NProfit/(self.Budget+Mkting),3)
            except: ROC = 'N/A'

            item = MovieItem()
            
            item['Parent'] = MojoSpider.Parent
            item['Name'] = Name
            item['Year'] = Year
            item['Date'] = Date
            item['Distrib'] = Distrib
            item['Genre'] = Genre
            item['Opening'] = Opening
            item['Domestic'] = Domestic
            item['Overseas'] = Overseas            
            item['Total'] = Total
            item['ParentRev'] = ParentRev
            item['Budget'] = self.Budget # self.variable_name => Why? we create a global scope variable that can be called anywhere in the Class 
            item['Mkting'] = Mkting
            item['GProfit'] = GProfit
            item['NProfit'] = NProfit
            item['ROC'] = ROC
               
            yield item


    def budget_backup(self, response): 

            tab2 = response.xpath('//*[@id="page_filling_chart"]/center').extract()            
      
            self.Budget = float(Selector(text=tab2[0]).xpath('//tr//a[.= ' + str(Name) + ']/../../../td/text()').extract()[1].encode('utf-8', 'ignore').replace('$','').replace(',',''))/1000000
            

    
     

    