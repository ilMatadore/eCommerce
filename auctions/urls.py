from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("<int:product_id>", views.product, name="product"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("remove_watchlist/<int:product_id>",
         views.remove_watchlist, name="remove_watchlist"),
    path("add_watchlist/<int:product_id>",
         views.add_watchlist, name="add_watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:category_id>",
         views.sort_by_category, name="sort_by_category")
]
