from ninja import NinjaAPI
from travels.api import router as travels_router

api = NinjaAPI()

api.add_router('travels/', travels_router)
