from pydantic import BaseModel
from typing import Optional


class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None

    def __str__(self):
        return f"Item[name:{self.name}, price:{self.price}, brand:{self.brand}]"


class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None

    def __str__(self):
        return f"Item[name:{self.name}, price:{self.price}, brand:{self.brand}]"



if __name__ == "__main__":
    print("Sample to instantiate class inheriting `pydantic BaseModel`:")
    print("============================================================")
    item1 = Item(name="item1", price=1.11, brand="brand1")
    print(item1)