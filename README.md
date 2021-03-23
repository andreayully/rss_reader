# Django rss_reader

Rss Reader built in Django with [feedparser](https://pythonhosted.org/feedparser/index.html) and Celery


## To run locally
**pre requirements Python 3.+ and Virtualenv**
1. Create virtual environment and activate environment  
`python3 -m venv venv`  
`source venv/bin/activate`

2. Clone repository   
`git clone https://github.com/andreayully/rss_reader.git`

3. Install requirements   
`pip install -r requirements.txt`  

4. Install Redis
https://redis.io/download  
And in a new terminal window, fire up the server `redis-server`  
`redis-cli ping` Redis should reply with PONG 

5. Runserver   
`python manage.py runserver`  

6. Starting the worker process. Open two new terminal windows/tabs  
`celery -A rss_reader worker -l info`  
`celery -A rss_reader beat -l info`

## What you can do  
* **Login as testuser**  
username= testuser   
password= test123*  
You can explorer diferents RSS Subcriptions  
![alt text](https://github.com/andreayully/rss_reader/blob/master/rss_list_2.png)

* **Or create a new user with the *Sing Up* option**

* Suscribe to new RSS feed with the **RSS Suscribe** button  

* Entries are updated every 12 hours via celery tasks
* You can see the update log in log_entries.txt  

### Tests available  
`python manage.py test`
