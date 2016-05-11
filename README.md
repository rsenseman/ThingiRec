# ThingiRec
ThingiRec is a content-based recommendation system for thingiverse.com users. The web app can be accessed [here](http://www.thingirec.xyz).

## Overview
ThingiRec uses item data from [thingiverse.com](http://www.thingiverse.com) to recommend to users other users with whom they should connect and parts that they may be interested in building. [Thingiverse.com](http://www.thingiverse.com) is a 3D printing hobbyist website where users share their 3D-printed creations. User recommendations are made by *content-based filtering*; cosine similarity is calculated between each of the user's parts and all other parts in the database for comparison. After the most similar items are found, the associated users are recommended to the input user.  

The goal in using content-based filtering is to connect users based on printing complications they might have. For example, User A who is interested in [ornate iphone cases](http://www.thingiverse.com/thing:65810) and User B who is interested in [automotive transmissions](http://www.thingiverse.com/thing:34778) may not connect based on their outwardly stated interests, but they are both interested in functional gears. Content-based filtering may match them.

[User A's Iphone Case](http://www.thingiverse.com/thing:65810)             |  [User B's Automotive Transmission](http://www.thingiverse.com/thing:34778)
:-------------------------:|:-------------------------:
![iphone_case](/readme_files/iphone_case.jpg)  |  ![transmission](/readme_files/transmission.jpg)

## The Process
The overall process of the project can be broken down into 4 steps. These steps will be detailed below:  
1. Data Collection  
2. Data Transformation  
3. Model Creation/Code Refactoring  
4. App Creation and Deployment  

##### 1) Data Collection
Items uploaded to thingiverse.com have a maximum item id of ~1,500,000, representing ~1.5 million items that have been uploaded to the site. All potential item pages were inspected and ~500,000 records were yielded from the scraping. Many items have been deleted or hidden from the site since it's inception. The item id, name, description, and associated username was scraped from each page using BeautifulSoup, requests, and pandas and was stored in a PostgreSQL database using psycopg2.  

The script used for scraping is [/thingiscrape/item_scrape_thingiverse.py](https://github.com/rsenseman/ThingiRec/blob/master/thingiscrape/item_scrape_thingiverse.py). In practice, this scraping was parallelized over 3 AWS instances to speed the collection.

##### 2) Data Transformation
Upon launch of [the web app](https://github.com/rsenseman/ThingiRec/tree/master/flask_app), all of the part names and descriptions are vectorized by the [sklearn TfidfVectorizer](http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html). The number of features was limited to 1000 to increase the speed of recommendation.

##### 3) Model Creation/Code Refactoring
When a username is entered, cosine similarity is calculated between each of the user's parts and all other parts in the database. From the most similar parts, the related usernames are taken and are recommended for connection  

The most challenging aspect of the project was creating recommendations in both a memory and time efficient manner. Through many iterations of code refactoring, the memory required for recommendations was reduced from <64 GB to <16 GB and the time requirement of a baseline recommendation was reduced from 20 minutes to 7 seconds.

##### 4) App Creation and Deployment
[The web app](https://github.com/rsenseman/ThingiRec/tree/master/flask_app) is written in Python using the Flask framework and is designed with a [Start Bootstrap](http://startbootstrap.com/) theme. The app is hosted on AWS.  

![The App, Live!](/readme_files/app_screenshot2.png)
