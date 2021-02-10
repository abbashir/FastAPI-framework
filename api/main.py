from typing import Optional

import aiofiles
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

fakedb = []


class Product(BaseModel):
    id: int
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.get("/")
def read_root():
    return {"welcome_message": "Greetings from Bashir"}


@app.get("/products")
def read_product():
    return fakedb


@app.get("/products/{product_id}")
def read_a_product(product_id: int):
    product = product_id - 1
    return fakedb[product]


@app.post("/products")
def add_product(product: Product):
    fakedb.append(product.dict())
    return fakedb[-1]


@app.put("/products/{product_id}")
def update_product(product_id: int, product: Product):
    product_id = product_id - 1
    product_old = fakedb[product_id]
    product_old.update(product)
    return {"message": "Product update successful"}


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    fakedb.pop(product_id - 1)
    return {"message": "product deletion successful"}


@app.post("/files/")
async def create_upload_file(uploaded_file: UploadFile = File(...)):
    file_location = f"D:/DjangoProject/fastAPI/api/{uploaded_file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())
    return {"info": f"file '{uploaded_file.filename}' saved at '{file_location}'"}
