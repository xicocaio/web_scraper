# Web Scraper
Simple web scraper with Google BigQuery integration

## Stack

The stack bellow was used mostly due to it's ease of installation, configuration and also efficiency and portability.
* Language: Python (3.5.2)
* Cloud Service: Google Cloud BigQuery (1.5.0)

## Pre-installation

This system was developed in Ubuntu 16.04, but will work properly on any other Operational System(OS X, Windows, etc.).

However, this guide will only include instructions for plugins and packages that are not already installed on this OS. For this reason, we assume that technologies like a python interpreter and SQLite are ready for use, and should not be on the scope of this document.

* Now install pipenv dependency manager:

```bash

$ pip install --user pipenv

```

## Project configuration

Now we'll start setting up the project.

* Clone the repo from github and change to project root directory.
After that install project dependencies and go topython virtual env, by running:

```bash
$ pipenv install
$ pipenv shell
```

* Download the service account key from google
[(instructions here)](https://cloud.google.com/bigquery/docs/reference/libraries).
Then, set the filepath to the json file in the local variable 'GOOGLE_APPLICATION_CREDENTIALS', by running:
```bash
$ export GOOGLE_APPLICATION_CREDENTIALS=path/to/file/google-service-key.json
```

**\* Here it was assumed that the user has properly set google cloud permissions**

## Running the project

Now we will run the project and get query answers

* The project will do the following actions
    1. Download the html of a product from a marketplace
    2. Parse the html and extract the data to a CSV file
    3. Load the csv data to Google BigQuery
    4. Query data directly from Google BigQuery

```bash
$ python app
```

* To run just the step 4 above, pass the argument step=query:

```bash
$ python app --step=query
```

* Console output example:
```bash

--- Starting webpages download ---

Page 1 finished
Page 2 finished
Page 3 finished
Page 4 finished
Page 5 finished

--- Webpages download finished successfully ---

--- Starting extraction of data to CSV ---
 
File /web_scraper/app/data/olx-sp-2018-08-29/page-5.html extraction starting
File /web_scraper/app/data/olx-sp-2018-08-29/page-5.html extraction finished
 
File /web_scraper/app/data/olx-sp-2018-08-29/page-1.html extraction starting
Warning: Some of the items downloaded in this file have missing data
File /web_scraper/app/data/olx-sp-2018-08-29/page-1.html extraction finished
 
File /web_scraper/app/data/olx-sp-2018-08-29/page-2.html extraction starting
File /web_scraper/app/data/olx-sp-2018-08-29/page-2.html extraction finished
 
File /web_scraper/app/data/olx-sp-2018-08-29/page-3.html extraction starting
Warning: Some of the items downloaded in this file have missing data
File /web_scraper/app/data/olx-sp-2018-08-29/page-3.html extraction finished
 
File /web_scraper/app/data/olx-sp-2018-08-29/page-4.html extraction starting
Warning: Some of the items downloaded in this file have missing data
File /web_scraper/app/data/olx-sp-2018-08-29/page-4.html extraction finished
 
Downloaded files removed

--- Data extraction finished ---

--- Starting file loading to cloud ---

Loaded 601 rows into web_scraper:product.

--- Finished file loading to cloud ---

--- Respondendo as perguntas ---
 
--> Qual o preço médio do produto por cidade?
Rio Grande da Serra : R$3000
Mauá : R$3000
Birigüi : R$3100
São Paulo : R$3143
Piracicaba : R$3150
Marília : R$3163
Bauru : R$3375
Jundiaí : R$3383
Osasco : R$3385
Santos : R$3400
São José do Rio Preto : R$3429
Guarulhos : R$3488
São José Dos Campos : R$3496
Santo André : R$3498
Sorocaba : R$3594
Barueri : R$3595
Ribeirão Preto : R$3603

--> Qual a cidade que mais possui ofertas do produto?
São Paulo : 192 ofertas

--> Liste os 5 mais baratos e o mais caro.
most expensive product : R$6100, iphone 8 plus 64g relogio apple watch 42mm, São Paulo, SP
least expensive products : R$1000, iphone 8 plus, São Paulo, SP
least expensive products : R$1000, iphone 8 para peça, São Paulo, SP
least expensive products : R$1000, iphone 8 plus, Mogi das Cruzes, SP
least expensive products : R$1000, iphone 8 plus (primeira linha), Santa Isabel, SP
least expensive products : R$1300, iphones 7 e 8  com os melhores preços aproveitem chamou levou, São Paulo, SP

```


## Further Improvements
* Job scheduler

    Adding a feature for scheduling each job separately with improve performance 

* Work for any site and product

    Right now the code only works for a product and marketplace, with minor adjustments it can work for multiple ones


## Final considerations

* Go play around! =)
