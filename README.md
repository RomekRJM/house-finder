# house-finder
Handy web crawler, that helps me find my perfect flat in Krakow!
Scrapes otodom.pl site, putting all flats in ElasticSearch.
Later uses advanced queries, to find flat matching location, price and couple other criterias 
and notifies about best ones via email.

# Installation
- Install Python 3 ( tested on 3.6 ): https://www.python.org/downloads/
- Install Elasticsearch 7.2: https://www.elastic.co/guide/en/elasticsearch/reference/7.2/install-elasticsearch.html

```
git clone https://github.com/RomekRJM/house-finder.git
pip install virtualenv
virtualenv venv
source venv/bin/activate
cd house-finder
pip install -r requirements.txt
```

Now you can edit run-me.sh file, and provide all required variables.
You can set it to run from cron, check crontab file.
