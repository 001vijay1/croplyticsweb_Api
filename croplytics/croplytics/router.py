from rest_framework import routers
from Api.viewsets import Userviewsets

router = routers.DefaultRouter()
router.register('Register',Userviewsets)

