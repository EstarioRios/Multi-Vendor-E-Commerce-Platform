from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Product.views import get_user_from_token
from .models import Product, Blog, OrderCard, Card, Comment
from .serializers import (
    BlogFullSerializer,
    CommentSerializer,
    CardSerializer,
    OrderCardSerializer,
)
import magic
import bleach


def sanitize_html_file(
    uploaded_file, allowed_tags=None, allowed_attributes=None, strip=True
):
    """
    Validate and sanitize an uploaded HTML file.

    Parameters:
        uploaded_file (UploadedFile): The uploaded file object.
        allowed_tags (list): List of allowed HTML tags. Default is basic text tags.
        allowed_attributes (dict): Dictionary of allowed attributes for each tag. Default is empty.
        strip (bool): If True, remove disallowed tags instead of escaping them.

    Returns:
        str: The sanitized HTML content.

    Raises:
        ValueError: If the file is not a valid HTML file or if processing fails.
    """
    # Default settings
    if allowed_tags is None:
        allowed_tags = ["p", "h1", "h2", "h3", "strong", "em", "ul", "ol", "li", "br"]

    if allowed_attributes is None:
        allowed_attributes = {}

    try:
        # Check file MIME type
        file_mime = magic.from_buffer(uploaded_file.read(1024), mime=True)
        uploaded_file.seek(0)  # Reset file pointer

        if file_mime != "text/html":
            raise ValueError("File must be of type HTML")

        # Read and decode content
        raw_content = uploaded_file.read().decode("utf-8")
        uploaded_file.seek(0)

        # Sanitize content using Bleach
        clean_content = bleach.clean(
            raw_content, tags=allowed_tags, attributes=allowed_attributes, strip=strip
        )

        return clean_content

    except UnicodeDecodeError:
        raise ValueError("Error reading file content - invalid format")
    except Exception as e:
        raise ValueError(f"File processing error: {str(e)}") from e


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_blog(request):
    """
    API endpoint to create a new blog post.
    Only store owners can create blogs.
    """
    # Get the user from the token
    user, response_error = get_user_from_token(request)
    if response_error:
        return Response(response_error)

    if user:
        if user.user_type != "store_owner":
            return Response(
                {"error": "Only store owners can create blogs"},
                status=status.HTTP_403_FORBIDDEN,
            )

        data = request.data
        product_id = data.get("product_id")
        title = data.get("title")
        description = data.get("description")
        content_file = request.FILES.get(
            "content_file"
        )  # Get the file from request.FILES

        # Validate required fields
        if not all([product_id, title, description, content_file]):
            return Response(
                {
                    "error": "product_id, title, description, and content_file are required"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Sanitize the HTML file
        try:
            sanitized_content = sanitize_html_file(content_file)
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if the product exists
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Create the blog post
        blog = Blog.objects.create(
            product=product,
            title=title,
            description=description,
            content_file=sanitized_content.encode(
                "utf-8"
            ),  # Save the sanitized content
        )

        # Clear the cache for related views
        cache.delete("all_blogs_cache")
        cache.delete(f"product_blogs_cache_{product_id}")

        # Serialize the created blog post and return it in the response
        serialized_blog = BlogFullSerializer(blog)
        return Response(serialized_blog.data, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])  # Specifies that this view only accepts DELETE requests
@permission_classes(
    [IsAuthenticated]
)  # Ensures that only authenticated users can access this view
def delete_blog(request):
    """
    Deletes a blog post. Only store owners and admins are allowed to perform this action.
    """

    # Retrieve the user from the request token
    user, response_error = get_user_from_token(request)
    if response_error:
        # If there's an error in retrieving the user, return the error response
        return Response(response_error)

    # Check if the user exists
    if user:
        # Verify if the user has the required permissions (store_owner or admin)
        if (user.user_type != "store_owner") or (user.user_type != "admin"):
            # If the user is not authorized, return a 403 Forbidden response
            return Response(
                {"error": "Only store owners and admins can delete blogs"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Extract the blog_id from the request query parameters
        data = request.data
        blog_id = data.query_params.get("blog_id")

        if not blog_id:
            return Response(
                {"error": "blog id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Find the blog post to be deleted using the blog_id
        target_blog = Product.objects.filter(id=blog_id).first()
        # Delete the blog post
        blog = target_blog.delete()

        # Clear the cache for related views
        cache.delete("all_blogs_cache")
        cache.delete(f"product_blogs_cache_{blog_id}")

        # Serialize the deleted blog post (optional, depending on your use case)
        serialized_blog = BlogFullSerializer(blog)
        # Return the serialized data with a 200 OK status
        return Response(serialized_blog.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_cart(request):
    """
    Retrieve the products in the user's shopping cart.

    Args:
        request (HttpRequest): The request object.

    Returns:
        Response: A JSON response containing the list of products in the cart.
    """
    # Get the user from the token
    user, response_error = get_user_from_token(request)
    if response_error:
        return Response(response_error)

    # Define cache key
    cache_key = f"user_cart_{user.id}"

    # Check if data exists in the cache
    cached_data = cache.get(cache_key)
    if cached_data:
        return Response({"cart": cached_data}, status=status.HTTP_200_OK)

    # Get the user's cart
    try:
        cart = Card.objects.get(user=user)
    except Card.DoesNotExist:
        return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

    # Get all order items in the cart
    order_items = OrderCard.objects.filter(card=cart)
    serialized_order_items = OrderCardSerializer(order_items, many=True)

    # Cache the serialized data for 10 minutes (600 seconds)
    cache.set(cache_key, serialized_order_items.data, timeout=600)

    return Response({"cart": serialized_order_items.data}, status=status.HTTP_200_OK)


@api_view(["PUT"])  # Specifies that this view only accepts PUT requests
@permission_classes(
    [IsAuthenticated]
)  # Ensures that only authenticated users can access this view
def update_blog(request):
    """
    Updates a blog post. Only store owners are allowed to perform this action.
    """

    # Retrieve the user from the request token
    user, response_error = get_user_from_token(request)

    # If there's an error in retrieving the user, return the error response
    if response_error:
        return Response(response_error)

    # Check if the user exists
    if user:
        # Verify if the user has the required permission (store_owner)
        if user.user_type != "store_owner":
            # If the user is not authorized, return a 403 Forbidden response
            return Response(
                {"error": "Only store owners can update blogs"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Extract data from the request
        data = request.data
        product_id = data.query_params.get(
            "product_id"
        )  # Get the product_id from query parameters
        title = data.query_params.get("title")  # Get the title from query parameters
        description = data.query_params.get(
            "description"
        )  # Get the description from query parameters
        content_file = data.FILES.get(
            "content_file"
        )  # Get the content file from uploaded files
        active = data.query_params.get(
            "active"
        )  # Get the active status from query parameters

        # Check if all required fields are provided
        if not all([product_id, title, description, content_file]):
            # If any required field is missing, return a 400 Bad Request response
            return Response(
                {
                    "error": "product_id, title, description, and content_file are required"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Sanitize the HTML file to ensure it's safe
        try:
            sanitized_content = sanitize_html_file(content_file)
        except ValueError as e:
            # If sanitization fails, return a 400 Bad Request response with the error message
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Clear the cache for related views
        cache.delete("all_blogs_cache")
        cache.delete(f"product_blogs_cache_{product_id}")

        # Update the blog post with the new data
        Blog.objects.filter(id=product_id).update(
            active=active,
            description=description,
            title=title,
            content_file=sanitized_content.encode(
                "utf-8"
            ),  # Encode the sanitized content to UTF-8
        )


@api_view(["GET"])
def blog_dependent_on_product(request):
    """
    Retrieve all blogs related to a specific product with caching.

    Args:
        request (HttpRequest): The request object containing query parameters.

    Returns:
        Response: A JSON response containing the list of blogs or an error message.
    """
    product_id = request.query_params.get("product_id")

    if not product_id:
        return Response(
            {"error": "product id is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    cache_key = f"product_blogs_{product_id}"
    cached_data = cache.get(cache_key)

    if cached_data:
        return Response({"product_blogs": cached_data}, status=status.HTTP_200_OK)

    product = Product.objects.filter(id=product_id).first()

    if not product:
        return Response(
            {"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

    product_blogs = product.blogs.all()
    product_blogs_serialized = BlogFullSerializer(product_blogs, many=True)

    cache.set(
        cache_key, product_blogs_serialized.data, timeout=600
    )  # Cache for 10 minutes

    return Response(
        {"product_blogs": product_blogs_serialized.data}, status=status.HTTP_200_OK
    )


@api_view(["GET"])  # Specifies that this view only accepts GET requests
def show_all_blogs(request):
    """
    Retrieve a list of all active blog posts, utilizing caching for optimization.

    Args:
        request (HttpRequest): The request object.

    Returns:
        Response: A JSON response containing the list of all blogs.
    """
    # Define cache key
    cache_key = "blogs_list"

    # Check if data exists in the cache
    cached_data = cache.get(cache_key)
    if cached_data:
        return Response({"blogs_list": cached_data}, status=status.HTTP_200_OK)

    # Retrieve all active blog posts from the database
    blogs_list = Blog.objects.filter(active=True)

    # Serialize the list of blog posts
    blogs_list_serialized = BlogFullSerializer(blogs_list, many=True)

    # Store serialized data in cache with a timeout of 10 minutes (600 seconds)
    cache.set(cache_key, blogs_list_serialized.data, timeout=600)

    # Return the serialized data with a 200 OK status
    return Response(
        {"blogs_list": blogs_list_serialized.data}, status=status.HTTP_200_OK
    )


@api_view(["GET"])  # Specifies that this view only accepts GET requests
def show_comments_dependent_on_blog(request):
    """
    Retrieve all comments related to a specific blog post with caching.

    Args:
        request (HttpRequest): The request object containing query parameters.

    Returns:
        Response: A JSON response containing the list of comments or an error message.
    """
    # Extract query parameters from the request
    data = request.query_params

    # Get the blog_id from query parameters
    blog_id = data.get("blog_id")

    # Check if blog_id is provided
    if not blog_id:
        return Response(
            {"error": "blog_id is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    # Define cache key
    cache_key = f"blog_comments_{blog_id}"
    cached_comments = cache.get(cache_key)

    if cached_comments:
        return Response({"comments": cached_comments}, status=status.HTTP_200_OK)

    # Retrieve the blog post with the given ID and ensure it is active
    try:
        blog = Blog.objects.get(active=True, id=blog_id)
    except Blog.DoesNotExist:
        # If the blog does not exist, return a 404 Not Found response
        return Response(
            {"error": "Blog does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

    # Retrieve all comments related to the blog post
    comments = blog.comments.all()

    # Serialize the comments
    comments_serialized = CommentSerializer(comments, many=True)

    # Cache the serialized data for 10 minutes (600 seconds)
    cache.set(cache_key, comments_serialized.data, timeout=600)

    # Return the serialized data with a 200 OK status
    return Response({"comments": comments_serialized.data}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_comment(request):
    """
    Create a new comment on a blog post.

    Args:
        request (HttpRequest): The request object containing the comment data.

    Returns:
        Response: A JSON response indicating success or failure.
    """
    # Retrieve the user from the token
    user, error_response = get_user_from_token(request)
    if error_response:
        return Response(error_response)

    data = request.data
    blog_id = data.get("blog_id")
    content = data.get("content")

    if not all([blog_id, content]):
        return Response(
            {"error": "blog_id and content are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        blog = Blog.objects.get(id=blog_id)
    except Blog.DoesNotExist:
        return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)

    # Create the comment
    Comment.objects.create(content=content, blog=blog, user=user)

    # Clear related comments cache
    cache.delete(f"blog_comments_{blog_id}")  # Added cache invalidation

    return Response({"message": "Comment created"}, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_comment(request):
    """
    Delete a comment from a blog post.
    Only the comment owner or an admin can delete the comment.

    Args:
        request (HttpRequest): The request object containing the comment data.

    Returns:
        Response: A JSON response indicating success or failure.
    """
    # Retrieve the user from the token
    user, error_response = get_user_from_token(request)
    if error_response:
        return Response(error_response)

    data = request.data
    blog_id = data.get("blog_id")

    blog = Blog.objects.filter(id=blog_id).first()
    if not blog:
        return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)

    if (user == blog.user) or (user.user_type == "admin"):
        blog.delete()

        # Clear related comments cache
        cache.delete(f"blog_comments_{blog_id}")  # Added line

        return Response(
            {"message": "Comment deleted"}, status=status.HTTP_204_NO_CONTENT
        )
    else:
        return Response(
            {"error": "You do not have permission to delete this comment"},
            status=status.HTTP_403_FORBIDDEN,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_product_to_cart(request):
    """
    Add a product to the user's shopping cart.
    If the product already exists in the cart, increment the order_time.
    If not, create a new order item in the cart.

    Args:
        request (HttpRequest): The request object containing product_id and order_time.

    Returns:
        Response: A JSON response indicating success or failure.
    """
    # Get the user from the token
    user, response_error = get_user_from_token(request)
    if response_error:
        return Response(response_error)

    # Extract data from the request
    data = request.data
    product_id = data.get("product_id")
    order_time = data.get("order_time", 1)

    if not product_id:
        return Response(
            {"error": "product_id is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response(
            {"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

    cart, created = Card.objects.get_or_create(user=user)

    try:
        order_item = OrderCard.objects.get(card=cart, product=product)
        order_item.order_time += order_time
        order_item.save()
        message = "Product quantity updated in the cart."
    except OrderCard.DoesNotExist:
        OrderCard.objects.create(card=cart, product=product, order_time=order_time)
        message = "Product added to the cart."

    # Clear user's cart cache
    cache.delete(f"user_cart_{user.id}")  # Added cache invalidation

    return Response({"message": message}, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def remove_product_from_cart(request):
    """
    Remove a product from the user's shopping cart.
    If the product exists in the cart:
      - If order_time > 1: decrement order_time
      - If order_time == 1: delete the order item

    Args:
        request (HttpRequest): The request object containing product_id.

    Returns:
        Response: A JSON response indicating success or failure.
    """
    # Get the user from the token
    user, response_error = get_user_from_token(request)
    if response_error:
        return Response(response_error)

    data = request.data
    product_id = data.get("product_id")

    if not product_id:
        return Response(
            {"error": "product_id is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response(
            {"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

    try:
        cart = Card.objects.get(user=user)
    except Card.DoesNotExist:
        return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        order_item = OrderCard.objects.get(card=cart, product=product)

        if order_item.order_time > 1:
            order_item.order_time -= 1
            order_item.save()
            message = "Product quantity decreased in the cart."
        else:
            order_item.delete()
            message = "Product removed from the cart."

    except OrderCard.DoesNotExist:
        return Response(
            {"error": "Product not found in the cart"}, status=status.HTTP_404_NOT_FOUND
        )

    # Clear user's cart cache
    cache.delete(f"user_cart_{user.id}")  # Added cache invalidation

    return Response({"message": message}, status=status.HTTP_200_OK)
