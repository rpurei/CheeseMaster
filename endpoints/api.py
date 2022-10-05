from .category.routes import router as category_router
from .content.routes import router as content_router
from .manufacturer.routes import router as manufacturer_router
from .order.routes import router as order_router
from .pickpoint.routes import router as pickpoint_router
from .price.routes import router as price_router
from .product.routes import router as product_router
from .production.routes import router as production_router
from .warehouse.routes import router as warehouse_router
from .users.routes import router as user_router
from .storage.routes import router as storage_router
from .reports.routes import router as report_router
from fastapi import APIRouter

router = APIRouter(prefix='/api')


@router.get('/')
async def root():
    return {'message': 'CheeseMaster online!'}

router.include_router(category_router)
router.include_router(content_router)
router.include_router(manufacturer_router)
router.include_router(order_router)
router.include_router(pickpoint_router)
router.include_router(price_router)
router.include_router(product_router)
router.include_router(production_router)
router.include_router(warehouse_router)
router.include_router(user_router)
router.include_router(storage_router)
router.include_router(report_router)
