# Essex County Council Website Link Scraper

This is a one-off project to test that redirects are in place, before a site is migrated to a new location.

## Running

There are a few steps.

###  Python

Ensure you have Python 3.9 installed, as well as pipenv. Then run the following:

```
pipenv install
```

###  Scraping a list of pages

Run

```
pipenv run scrapy runspider scraper.py -o ./output/output.csv
```

###  Modifying your hosts file

Add a line to your hosts file (using something like `sudo nano /etc/hosts`) for the site that you're trying to test. This is needed because the DNS will point to the old website and will not enable you to test anything.

### Testing that redirects are working

Run

```
pipenv run python test_redirects.py
```

The output will go to `./output/redirect_test_output.xlsx`
