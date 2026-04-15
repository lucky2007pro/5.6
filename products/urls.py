from django.urls import path
from .views import (
    IndexView,
    ProductDetailView,
    comment_create,
    update_comment,
    delete_comment,
    my_comments,
    saved,
    like,
    user_saveds,
    user_likes,
    user_recently,
)

urlpatterns = [
    path("",IndexView.as_view(),name="index"),
    path("product/<uuid:id>/",ProductDetailView.as_view(),name="product_detail"),
    path("product/<uuid:product_id>/comment/", comment_create, name="comment_create"),
    path("comment/<uuid:comment_id>/update/", update_comment, name="update_comment"),
    path("comment/<uuid:comment_id>/delete/", delete_comment, name="delete_comment"),
    path("product/<uuid:product_id>/saved/", saved, name="saved"),
    path("product/<uuid:product_id>/like/", like, name="like"),
    path("saved/", user_saveds, name="saved_products"),
    path("likes/", user_likes, name="liked_products"),
    path("comments/", my_comments, name="my_comments"),
    path("recently/", user_recently, name="recently_products"),
]
