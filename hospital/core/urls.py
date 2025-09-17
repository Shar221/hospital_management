from rest_framework import routers
from .views import PatientViewSet, AppointmentViewSet, InvoiceViewSet

router = routers.DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'invoices', InvoiceViewSet)

urlpatterns = router.urls