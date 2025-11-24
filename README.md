# Wool Finder - your gateway to the wool world! 

---

## About Project
Wool finder portal which can scrape products from desired shops to compare prices.
Made with:
- Django
- SQL-lite Database to store data
- Cloudscraper to bypass Cloudflare protection

Currently, our application can scrape desired products from:
1. Wollplatz.de 


## How to use

1. Clone this project: `git clone https://github.com/31f/woolfinder.git`
2. Run Database migrations: `python manage.py migrate`
3. Run products refresh command: `python manage.py refresh_wool_base`
4. Check logs 
5. You can use Django Admin to review scraped Products
   - Run command: `python manage.py createsuperuser `
   - Go to Admin page: http://127.0.0.1:8000/admin/


## Tests

Run simple test: `python manage.py test`


## Further Development
This is only example how we can start this application and make it easy scalable.
It needs more time to make it really beautiful and to polish the existing scraper.
But in future we can easily:
- Add more Shops and specific Scrapers
- Scrape more Product details
- Set `refresh_wool_base` as Cron job to always have updated Products data
- Create web page to browse and filter all our product offers, which we scraped to our database.
