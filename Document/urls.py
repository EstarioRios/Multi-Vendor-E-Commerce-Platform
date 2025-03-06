from django.urls import path
from . import views

urlpatterns = [
    # Blog URLs
    path("blogs/create/", views.create_blog, name="create_blog"),
    path("blogs/delete/", views.delete_blog, name="delete_blog"),
    path("blogs/update/", views.update_blog, name="update_blog"),
    path("blogs/by-product/", views.blog_dependent_on_product, name="blog_by_product"),
    path("blogs/all/", views.show_all_blogs, name="show_all_blogs"),
    # Comment URLs
    path(
        "comments/by-blog/", views.show_comments_dependent_on_blog, name="show_comments"
    ),
    path("comments/create/", views.create_comment, name="create_comment"),
    path("comments/delete/", views.delete_comment, name="delete_comment"),
    # Cart URLs
    path("cart/add/", views.add_product_to_cart, name="add_to_cart"),
    path("cart/remove/", views.remove_product_from_cart, name="remove_from_cart"),
]
