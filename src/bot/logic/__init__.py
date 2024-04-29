from .start import start_photographer
from .add_agency import add_agency_router
from .add_photosession import add_photosession_router
from .add_service import add_service_router
from .registration import register_user

routers = (start_photographer, add_agency_router, add_photosession_router, add_service_router, register_user)
