## Python:Using Alternative Data to Anticipate Stocks Momentum: the case for movie stocks and weekly box office data
Web scraping box office data and creation of weekly indices to anticipate a stock price and earnings momentum for “movie” stocks (e.g. Lionsgate) 

## Data Sources:
- Python has been used for web scrapping using both Beautiful soup (top-down analysis) and Scrapy (company-specific information) libraries.
- Data sources are the websites "Box Office Mojo" and "The-numbers.com".

## Using Alternative Data to build weekly Profitability Indices for each stock:
- Each stock box office profitability index is constructed using using weekly box office figures and industry assumptions (marketing costs, theater rebate rates, etc) gathered from analyzing the fundamentals of the cinema and movie production business.
- Weekly box office indices add interim period information that allows us to predict abnormal returns (stock price return over benchmark) for our parent company stocks.
- Sell-side analysts take time to incorporate the newly gathered box office information into the quarterly and annual estimates. Hence, the weekly box office profitability indices anticipate earnings momentum.
- In other words, a quantamental stock scoring system could incorporate these weekly indices to enhance the overall "earnings momentum" score of the model that usually is fed only by conventional sell-side analysts earnings revisions.   

## Notes:
- Read the related post at NYCDSA blog to get more familiar with the data as well as to understand the specific case of movie stocks and box office data: https://nycdatascience.com/blog/student-works/web-scrapping-weekly-box-office-figures/
