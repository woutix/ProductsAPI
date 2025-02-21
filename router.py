from fastapi import Depends, APIRouter, Header, Query, HTTPException
from uuid import UUID

from database.repositories.product import ProductRepository
from schemas.product import ProductSchema, ProductAddSchema, ProductResponseSchema

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

# Проверка хедера и доступ к данным
async def check_authorization(x_test_authorization: str = Header(...)):
    
    if x_test_authorization != "x-test-key":  
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True


@router.post("/", response_model=ProductResponseSchema)
async def add_products(
        product_data: ProductAddSchema, authorization: bool = Depends(check_authorization)
) -> ProductResponseSchema:
    if not product_data.name or len(product_data.name.strip()) == 0:
        raise HTTPException(
            status_code=400,
            detail="Product name cannot be empty"
        )
    
    if  product_data.price < 0:
        raise HTTPException(
            status_code=400,
            detail="Product price must be a positive number"
        )
    
    if product_data.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Amount is required"
        )

    products = await ProductRepository.add_one(product_data)
    
    return ProductResponseSchema(id=products.id, name=products.name, price=products.price, amount=products.amount)

@router.get("/", response_model=list[ProductResponseSchema])
async def get_products(skip: int = Query(0, ge=0), limit: int = Query(10, le=100)) -> list[ProductSchema]:
    products = await ProductRepository.find_all(skip=skip, limit=limit)
    if products:
            return products
    else:
            raise HTTPException(status_code=404, detail="No products found")

@router.get("/{product_id}")
async def get_product_by_id(product_id: str) -> dict:
    product = await ProductRepository.find_by_id(UUID(product_id))
    if product:
        return {"product": product}
    else:
        raise HTTPException(status_code=404, detail="Product not found")

@router.delete("/{product_id}")
async def delete_product_by_id(product_id: str) -> dict:
    success = await ProductRepository.delete_by_id(UUID(product_id))
    if success:
        return {"message": "Product deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Product not found")

@router.put("/{product_id}")
async def update_product_by_id(product_id: str, product_data: ProductAddSchema) -> dict:
    updated_product = await ProductRepository.update_by_id(UUID(product_id), product_data)
    if updated_product:
        return {"message": "Product updated successfully", "product": updated_product}
    else:
        raise HTTPException(status_code=404, detail="Product not found")
