# abstract-prep

### How to get started:

Get the project:

```
git clone https://github.com/FlorianGraef/abstract-prep.git
```

Change to the project directory and create a new python environment using python >= 3.8 :
```
python3 -m venv venv/
```

Activate it
```
source ./venv/bin/activate
```

install all requirements:
```
pip install -r requirements.txt
```

start the API:
```
uvicorn abstract_prep.main:app 
```

With the API up and running the API documentation is available under http://127.0.0.1:8000/docs#/ (Swagger) or http://127.0.0.1:8000/redoc (ReDoc) and gives information about the three endpoints:

1. /preprocess/abstracts/
   POST expects a JSON object to be posted consisting of abstract_id and abstract field.
   E.g.:
   
```
{
  "abstract_id": "345",
  "abstract": "test to ,.markdown"
}
```

  The response will be a JSON object of the same form with a preprocessed abstract (stripped out punctuation and removed stopwords.

```
{
    "abstract_id": "345",
    "abstract": "test markdown"
}
```

2. /abstracts/ GET

Gets a list of all abstracts in the DB or, if the abstract_id parameter is provided, attempts to retrieve the specific abstract by abstract_id.

3. /abstracts/ POST

This endpoint allows as well to post abstracts in the afore-mentioned format to persist them in the DB. The query parameter "preprocess" toggles stopword and punctuation removal.

To populate a persisted shelve database file run:
```
python3 abstract_prep/cleaner.py /home/florian/Coding/abstract_test_data_file.txt
```

this will preprocess the textfile and persist the cleaned abstracts to the shelve database file in the project base directory.

