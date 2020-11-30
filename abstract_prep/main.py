import shelve
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from abstract_prep import cleaner


class Abstract(BaseModel):
    abstract_id: str
    abstract: str


app = FastAPI()


@app.post("/preprocess/abstracts/")
async def preprocess_abstract(abstract: Abstract):
    """
    http POST an abstract in JSON format. Yields the preprocessed abstract.
    :param abstract: abstract in JSON format
    :return: preprocessed abstract in JSON format
    """
    abstract.abstract = cleaner.preprocess_abs(abstract.abstract)
    return abstract


@app.get("/abstracts/")
async def list_abstracts(abstract_id: Optional[str] = None):
    """
    get a list of all abstracts or get specific one if it exists
    :param abstract_id:
    :return:
    """
    with shelve.open("adb") as adb:
        if abstract_id:
            if abstract_id not in adb.keys():
                raise HTTPException(status_code=404, detail="Item not found")
            else:
                abstract_body = adb[abstract_id]

                abstract = Abstract(abstract_id=abstract_id, abstract=abstract_body)
                return abstract
        else:
            return dict(adb)


@app.post("/abstracts/")
async def add_abstract(abstract: Abstract, preprocess: Optional[bool] = False):
    """
    Takes an abstract json object and posts it to the DB
    :param abstract:
    :param preprocess:
    :return:
    """
    if preprocess:
        abstract.abstract = cleaner.preprocess_abs(abstract.abstract)

    with shelve.open("adb") as adb:
        adb[abstract.abstract_id] = abstract.abstract

    return abstract
