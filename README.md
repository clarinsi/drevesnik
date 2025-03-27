# Drevesnik Service for Querying Dependency Treebanks 

Fork of [dep_search](https://github.com/TurkuNLP/dep_search) with additional features like random search, xpos search or search for short sentences.

## Set up

Requires docker

### Set up the base image required for later steps

Run `docker build -t drevesnik_base -f Dockerfile_service_base .` in the root of this project.


### Set up indexes

To run this project you first need to build indexes from conllu databases. Location of the indexes when the application is run is determined in `docker-compose.yml` with the `INDEXES_FOLDER` volume.

Create a folder with conllu database files. For each conllu file add a json metadata file with
the same name as conllu file.

Metadata json file should contain:
- **name** - Name of the database.
- **<lang>_desc** - Html name and describtion of the db used on the first page for each <lang> language. Slovenian language sl should be supported by default. Proposed form: `<b>name</b><br> describtion`
- **priority** - (optional) Defines how hight the database will be shown on the first page. Lower number gives higher priority. If no number is given it will assume the lowest priority.

Set up the corpra mounted folder in `Dockerfile_build_dataset.yml` to point to the conllu folder and the output folder to the folder where database indexes will be generated.

Run `docker-compose -f docker-compose-build-dataset.yml up --build` in the root of this project.

### Set up config folder

Config folder location is determined in `docker-compose.yml` with the `CONFIG_FOLDER` volume.

#### Set up cached calls

In each line of `<config_folder>/cache_calls.txt`, there is a call that is executed when this service is started and its results are
cached forever to ensure that some queries are executed almost instantly. Each line contains parameters of query separated with
tabulator.

Parameters:

* **Databases**: Names of the databases to be queried are separated with a comma. ex: *SSJ,SST*
* **Query**: Query string. ex:  *_ <nsubj _*
* **Language**: Language of the query (should be *sl*)
* **Limit**: Maximum number of sentences returned.
* **Case**: Value true if you want case insensitive search otherwise value false.
* **Random**: Value true for random hits otherwise false
* **Short sentence search** Value true for hits with sentences with 15 or fewer tokens otherwise false.
* **Ticket**: Name of the ticket where the query will be saved (important for the URL where query results will appear) (should not contain `.`,`/`,`_`).


Each of these queries can then be accessed at http://localhost/drevesnik/show/Ticket/Language/0/10.

#### Set up help page

For Slovene and English, there is a help page located on http://localhost/ for slovenian and http://localhost/<lang>/ for other languages.
Help page is generated from a markdown file saved in `<config_folder>/dep-search_query-lang_original_<lang>.md` files.

#### Set up statistics translations

Create `<config_folder>/statistics_translations_<lang>` files for each language. There are some examples for slovenian and english.

#### Set up statistics translations

Create `<config_folder>/html_translations/<lang>` files for each language. There are some examples for slovenian and english.

#### Set up Branding

Put all brands in `<config_folder>/branding.json` the same way as in the example file. 

All brandings should have:

- url - Web page link.
- image - Image url. Can also be image from `api_gui\static` folder like the examples in `<config_folder>/branding.json`.
- alt - Text that is shown if image url is not accessible.

#### Run the project with docker

Run 

```docker-compose up --build```

to build and run this project. The home page of this service can be accessed at http://localhost/drevesnik.


## Project structure

## dep_search 

Folder `dep_search` contains all logic behind querying parsed sentences. The core script is `dep_search/query.py`

To run locally, cython scripts need to be built with file `setup.py` by running `pip install . -e` in the root of this project.

## api_gui 

Folder `api_gui` contains the flask web application. The core script is `api_gui/api.py` where you can find all the endpoints.
Folder `api_gui/templates` contains all the HTML templeates and folder `api_gui/static` contains CSS and JSS scripts and images.

<a href="http://www.clarin.si/info/about/"><img src="https://gitea.cjvt.si/lkrsnik/dependency_parsing/raw/branch/master/logos/CLARIN.png" alt="drawing" height="80"/></a>
<a href="https://www.cjvt.si/en/"><img src="https://gitea.cjvt.si/lkrsnik/dependency_parsing/raw/branch/master/logos/CJVT.png" alt="drawing" height="80"/></a>
<a href="http://www.arrs.si/"><img src="api_gui/static/arrs.png" alt="arrs" height="80"/></a>
