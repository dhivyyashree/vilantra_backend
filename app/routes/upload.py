from fastapi import APIRouter, Form, File, UploadFile, HTTPException
from typing import List
import json
from datetime import datetime
from app.db.mongodb import save_product_to_db
from app.db.cloudinary_config import upload_image_to_cloudinary

router = APIRouter()

@router.post("/")
async def upload_product(
    title: str = Form(...),
    original_price: float = Form(...),
    discount_price: float = Form(...),
    category: str = Form(...),
    description: str = Form(...),
    variants: str = Form(...),  # JSON string
    images: List[UploadFile] = File(...)
):
    try:
        variant_data = json.loads(variants)
        image_map = {}

        for file in images:
            # Expect filename format: "blue_center_1.jpg"
            name_parts = file.filename.split("_")
            if len(name_parts) < 2:
                raise ValueError(f"Invalid filename format: {file.filename}")

            color = name_parts[0].strip().lower()
            focus = name_parts[1].strip().lower()

            url = await upload_image_to_cloudinary(file.file)

            image_obj = {"url": url, "focus": focus}
            image_map.setdefault(color, []).append(image_obj)

        for variant in variant_data:
            color_key = variant["color"].strip().lower()
            variant["images"] = image_map.get(color_key, [])

        product_doc = {
            "title": title,
            "original_price": original_price,
            "discount_price": discount_price,
            "category": category,
            "description": description,
            "variants": variant_data,
            "created_at": datetime.utcnow()
        }

        inserted_id = await save_product_to_db(product_doc)
        return {"message": "Product uploaded", "id": str(inserted_id)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
