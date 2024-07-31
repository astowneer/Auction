from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("index_category", views.index_category, name="index_category"),
    path("add_watchlist/<int:id>", views.add_watchlist, name="add-watchlist"),
    path("delete_watchlist/<int:id>", views.delete_watchlist, name="delete-watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("bid/<int:id>", views.bid, name="bid"),
    path("listing_close/<int:id>", views.listing_close, name="listing-close"),
]
