# dep_search_slo

Fork of [dep_search](https://github.com/TurkuNLP/dep_search) with additional features like random search, xpos search or search for short sentences.

## Set up

Requires docker and python3.

#### Set up database

Run the` build_index.py` script in the root of the project for every conllu file:

```sh
cat <location_of_conllu_file> | python3 build_index.py --lang sl --d <name_of_db>
```
Copy generated folder to the corpus folder.

Add description for the db in the `api_gui/db_desc.json` if needed:

```
"<name_of_db>": "<b><shown_name_of_db></b><br> description of the db"
```

To use xpos search you will need to generate xpos tags list for each corpus.
To do that you will have to first set up dictionary conllu_files in `generate_xpos_tags.py`.
Each entry in dictionary should be `"<name_of_db>": "<location_of_conllu_file>"`. After the dictionary
is filled with entries for each db run it to generate the `xpos_tags.json` file.

#### Set up cached calls

In each line of `api_gui/cache_calls.txt`, there is a call that is executed when this service is started and its results are
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

For Slovene and English, there is a help page located on http://localhost/ and http://localhost/en/.
Help page is generated from a markdown file saved in `dep-search_query-lang_original.md` and `dep-search_query-lang_original_en.md`


#### Run the project with docker

Run 

```
docker-compose up --build
```

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
