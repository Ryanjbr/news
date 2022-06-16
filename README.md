# YOUR PROJECT TITLE
#### Video Demo:  <URL HERE>
#### Description:
"Piano Pedagogy News" is a web app that scrapes articles from various news sites and blogs, displays said articles in reverse chronological order, and allows users to favorite articles to be saved for later.
##### News:
The "News" section of the app draws articles from Google News. It does this using the "pygooglenews" library. Articles are added to the "news.db" database under the "news" table. The index page of the app then draws from this SQL database to generate its list. For ease of sorting, datetimes are converted to integers before they are put into the database.
##### Blogs:
The "Blogs" section of this app functions similarly, but because the articles are sourced from several different sites, a different function had to be written for each site. The three sites that are currently used are "Piano Adventures Blog," "Color in my Piano," and "iPad Music Ed." To gather the articles for this site, the Beautiful Soup library was used. This library uses HTML tags to find pieces of information, and since each site organizes its HTML somewhat differently, the HTML tags each function searches for are changed from one another.
###### Favorites:
