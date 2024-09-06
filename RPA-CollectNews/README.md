# RPA - Collect News

This RPA automates the process of extracting news from the website "https://www.aljazeera.com/" and exporting it to an Excel file.

## Parameters:

The process must process 2 parameters:
  - search phrase
  - number of months for which you need to receive news.
      * Example of how this should work: 
          * 0 or 1 - only the current month,  
          * 2 - current and previous month,  
          * 3 - current and two previous months,  
          * and so on


## Process

1. Get process parameters:
    * search phrase
    * number of months for which you need to receive news.
2. Open the site by following the link
    * Enter the search phrase in the search tool
    * Get the values: title, date, and description.
3. Filter data by date range period and store it in an Excel file:
    * title
    * date
    * description (if available)
    * picture filename
    * count of search phrases in the title and description
    * True or False, depending on whether the title or description contains any amount of money
        * Possible formats: $11.1 | $111,111.11 | 11 dollars | 11 USD
    * Link to the news
    * Link to image
4. Download news picture.

## Main features in this challenge

1. PEP8 compliant
2. OOP
3. Fault-tolerant architecture
4. Robocorp browser selenium
5. Explicit waits
6. Best RPA practices
7. Logging