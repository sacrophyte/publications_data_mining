# Experts

At this point, I have only been asked to aggregate the number of publications per year over a five-year span for select faculty, and also to list each of those publications (two different requests, two different scripts). Uses the "Experts" University of Illinois portal for Elsevier Scopus via Pure 59 API calls.

## Scripts
*get_author_pubs_by_category.py*   
Retrieves a list of faculty via a csv on box.com. Since the default API calls for the persons.research_outputs endpoint defaults the number of publications that are retrieved with no parameter avaialbe to "get all", I first issue a call to get the count of publications for each author, and then using the count I grab that number of publications for that author. As I am using the JSON interface, there are known bugs when Pure 59 returns data (usually related to XML) and I strip them out of the returned data. Additionally, I have not yet found an endpoint or API parameter that lets me format the generated output exactly the way I require, so I have to manipulate the data quite heavily once I receive it. The cleaned data is then stored in another CSV, which I manually upload to box.com for the rest of the team to consume.

### Current
Right now, the list of faculty is provided via an Excel spreadsheet on box.com (private University link). I had a lot of difficulty getting the python APIs working correctly with box.com for spreadsheets (*everything* has to be streamed?!?), so I manually conver the facaulty name and email address to a comma-seperated-values (csv) text file. The python scripts read from this text file via the box.com file id, so if the file changes for any reason, a new box.com file id has to be provided as a hardcoded variable. I have not found a good way to simply search for a specific file. I am sure there are ways to do that, but it was not a high enough priority for me.

### Future
In the near future, I hope to migrate the list of faculty to a database, and have my python scripts interact direction with the database, both to retrieve faculty lists, and also to store results.
