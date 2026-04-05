from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from supplements.views import SupplementsView, NewSuplementView, SupplementDetailView, SupplementUpdateView, SupplementDeleteView, CategorySupplementView
from accounts.views import register_view, login_view, logout_view
from supplements.cart_views import add_to_cart, cart_view, remove_item, finalize_order



urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('register/', register_view , name='register'),
    path('new_supplement/', NewSuplementView.as_view(), name='new_supplement'),
    path('supplements/', SupplementsView.as_view(), name='supplements'),
    path('category/<slug:slug>/', CategorySupplementView.as_view(), name='category_supplement'),
    path('supplement/<int:pk>/', SupplementDetailView .as_view(), name='supplement_detail'),
    path('supplement/<int:pk>/update/', SupplementUpdateView.as_view(), name='supplement_update'),
    path('supplement/<int:pk>/delete/', SupplementDeleteView.as_view(), name='supplement_delete'),
    path("cart/", cart_view, name="cart"),
    path("carrinho/adicionar/<int:variant_id>/", add_to_cart, name="add_to_cart"),
    path("cart/remove/<str:key>/", remove_item, name="remove_item"),
    path("cart/checkout/", finalize_order, name="checkout"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
