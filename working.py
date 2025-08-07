import fastapi
from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional
from item_model import Item, UpdateItem

import logging
from rich.logging import RichHandler

# --------- Configure logger --------- #
## normal configuration
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
# )
# logger = logging.getLogger(__name__)

## using rich
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()]
)
logger = logging.getLogger("rich")

#---------------------------------------#

app = FastAPI()

#
# inventory = {
#         1: {
#             "name": "Milk",
#             "price": 3.99,
#             "brand": "Regular"
#         },
#         2: {
#             "name": "Sugar",
#             "price": 1.99,
#             "brand": "Fine-Sugar"
#         }
#     }

inventory = {
        1: Item(name="Milk", price=3.99, brand="Regular"),
        2: Item(name="Sugar", price=1.99, brand="Fine-Sugar")
    }

@app.get("/")
def home():
    logger.info("Home endpoint accessed.")
    return { "Data": "Testing"}


@app.get("/about")
def about():
    return { "Data": "About" }


@app.get("/get-inventory")
def get_inventory():
    return { "Data": inventory }


'''----- Path parameters [GET] -----'''
# single path parameter
# @app.get("/get-item/{item_id}")
# def get_item_by_id(item_id: int): # use type hint to indicate to FastAPI expected path type
#     return inventory[item_id]


# multiple path parameter
@app.get("/get-item/{item_id}/{message}")
def get_item_by_id(item_id: int, message: str): # use type hint to indicate to FastAPI expected arg type
    res = f"input id= {item_id}, name= {inventory[item_id]["name"]}, price= {inventory[item_id]["price"]}, brand= {inventory[item_id]["brand"]}, message={message}"
    return res


# adding constraints to path parameters
@app.get("/get-item/{item_id}")
def get_item_by_id(item_id: int = Path(description="The ID of the item you would like to view", ge=1)):
    return inventory[item_id]

'''----- Query parameters [GET] -----'''
# required query parameter
# @app.get("/get-item-by-name")
# def get_item(item_name: str):
#     for item_id, item in inventory.items():
#         if item.name.lower() == item_name.lower():
#             return inventory[item_id]
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail="Item name not found."
#     )


# optional query parameter
# @app.get("/get-item-by-name")
# # def get_item(item_name: str = None): # works as it is for optional query parameter
# def get_item(item_name: Optional[str] = None): # following best practices
#     for item_id, item in inventory.items():
#         if isinstance(item_name,str): # check str object for .lower() use
#             if item.name.lower() == item_name.lower():
#                 return inventory[item_id]
#         else: # normal equal check
#             if item.name == item_name:
#                 return inventory[item_id]
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail="Item name not found."
#     )


# multiple query parameters
@app.get("/get-item-by-name")
# def get_item(item_name: Optional[str] = None, add_query: int): # result in `non-default parameter follows default parameter`
# def get_item(add_query: int, item_name: Optional[str] = None ): # fix by rearranging default parameter before non-default parameter
def get_item(*, item_name: Optional[str] = None, add_query: int): # fix by adding asterisk as first arg - indicating let function accept unlimited positional args followed by keyword args
    logger.info(f"additional_query= {add_query}")
    for item_id, item in inventory.items():
        if isinstance(item_name, str): # check str object for .lower() use
            if item.name.lower() == item_name.lower():
                return inventory[item_id]
        else: # normal equal check
            if item.name == item_name:
                return inventory[item_id]
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Item name not found."
    )


'''----- Combining Path & Query parameters [GET] -----'''
@app.get("/get-by-name/{message}")
def get_item(*, message: str, item_name: Optional[str] = None, add_query: int): # order of args does not matter for this case - path parameter `message` can be anywhere
    logger.info(f"message= {message}")
    logger.info(f"additional_query= {add_query}")
    for item_id, item in inventory.items():
        if isinstance(item_name,str): # check str object for .lower() use
            if item.name.lower() == item_name.lower():
                return inventory[item_id]
        else: # normal equal check
            if item.name == item_name:
                return inventory[item_id]
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Item name not found."
    )


'''----- Request Body [POST] -----'''
@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Item ID already exists."
        )
    inventory[item_id] = item
    return inventory[item_id]


'''----- Update [PUT] -----'''
@app.put("/update-item/{item_id}")
def update_item(item_id: int, update_item: UpdateItem):
    if item_id not in inventory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item ID not found."
        )

    item = inventory[item_id]
    if update_item.name != None:
        item.name = update_item.name
    if update_item.price != None:
        item.price = update_item.price
    if update_item.brand != None:
        item.brand = update_item.brand

    return inventory[item_id]


'''----- Delete [DEL] -----'''
@app.delete("/delete-item")
def delete_item(item_id: int = Query(description="The ID of item to be deleted")):
    if item_id not in inventory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item ID not found."
        )
    item = inventory[item_id]
    del inventory[item_id]
    return {"Success" : f"{item} deleted."}
