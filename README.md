# yellowPages_crawler
Scrapes Australian yellowpages.com.au and outputs companies to .csv with contact information

NOTE: To use program you need to have chrome webdriver installed, and change line 37 in code to refer to the location of your webdriver

The code asks three questions to help you scrape contact information from yellowpages.com.au: 

(1) What you want to search on. It's worthwhile to browse yellowpages.com.au first to determine what keywords will match your criteria. Also, don't use special characters like & as the code has not been optimized to handle these.

(2) Where do you want to search. This allow you to restrict the search criteria to e.g. a state or city. Leave blank or type "Australia" if you do not want to restrict it.

(3) How many pages do you want to scrape. Each page with yellowpages.com.au search results includes 35 contacts. The code can browse multiple pages, but doing so requires the code to open a new chrome window which can be time consuming. This question has therefore been added to restrict the number of pages to scrape. Note that no matter how many results the search query produces on yellowpages, yellowpages only allows you to see the first 30 pages, i.e. 1050 results. 

(4) Which page do you want to start on. This feature has been added to allow you to start from the search results on e.g. page 5 in case you've already scraped pages 1-4. This makes it easier to scrape in batches. 

