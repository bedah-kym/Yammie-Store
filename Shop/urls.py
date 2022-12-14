from django.conf import settings
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views

app_name='Shop'
urlpatterns = [
    path('home/',views.homeview.as_view(),name='home'),
    path('product/<int:product_id>/',views.productview,name='product'),
    path('deletecomment/<int:product_id>/',views.deletecomment,name='delete-comment'),
    path('category/<str:category>/',views.categoryview.as_view(),name='categories'),
    path('checkout/',views.checkoutview,name='checkout'),
    path('agent_info/',TemplateView.as_view(template_name="Shop/agent_info.html"),name='agent-info-page'),
    path('redeem/',views.redeem,name='redeem'),
    path('order-summary/',views.ordersummary,name='order-summary'),
    path('order-success/',views.ordersuccess,name='order-success'),
    path('add_to_cart/<int:product_id>/',views.add_to_cart,name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/',views.remove_from_cart,name='remove_from_cart'),
    path('remove_singleitem_from_cart/<int:product_id>/',views.remove_singleitem_from_cart,name='remove_singleitem_from_cart'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
