# from fastapi import APIRouter
from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.db.mongodb import save_product_to_db, collection

router = APIRouter()

@router.get("/")
async def get_all_products():
    try:
        products_cursor = collection.find()
        products = []
        async for product in products_cursor:
            product["_id"] = str(product["_id"])  # convert ObjectId to string
            products.append(product)
        return products
    except Exception as e:
        return {"error": str(e)}
    

    
@router.get("/designer-sarees")
async def get_designer_sarees():
    try:
        products_cursor = collection.find({"category": "designer sarees"})
        products = []

        async for product in products_cursor:
            product["_id"] = str(product["_id"])  # Convert ObjectId to string
            products.append(product)

        return products
    except Exception as e:
        return {"error": str(e)}
@router.get("/{product_id}")
async def get_product_by_id(product_id: str):
    try:
        if not ObjectId.is_valid(product_id):
            raise HTTPException(status_code=400, detail="Invalid product ID format")

        product = await collection.find_one({"_id": ObjectId(product_id)})
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        product["_id"] = str(product["_id"])
        return product
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
@router.post("/")
async def create_product(product: dict):
    try:
        inserted_id = await save_product_to_db(product)
        return {"message": "Product saved", "id": str(inserted_id)}
    except Exception as e:
        return {"error": str(e)}
