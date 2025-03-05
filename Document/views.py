from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Product.views import get_user_from_token
from .models import Product, Blog
from .serializers import BlogFullSerializer
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

        # Serialize the deleted blog post (optional, depending on your use case)
        serialized_blog = BlogFullSerializer(blog)
        # Return the serialized data with a 200 OK status
        return Response(serialized_blog.data, status=status.HTTP_200_OK)


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
    Retrieve all blogs related to a specific product.

    Args:
        request (HttpRequest): The request object containing query parameters.

    Returns:
        Response: A JSON response containing the list of blogs or an error message.
    """
    # Get the product_id from query parameters
    product_id = request.query_params.get("product_id")

    # Check if product_id is provided
    if not product_id:
        return Response(
            {"error": "product id is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    # Retrieve the product
    product = Product.objects.filter(id=product_id).first()

    # Check if the product exists
    if not product:
        return Response(
            {"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

    # Retrieve all blogs related to the product
    product_blogs = product.blogs.all()

    # Serialize the blogs
    product_blogs_serialized = BlogFullSerializer(product_blogs, many=True)

    # Return the serialized data
    return Response(
        {"product_blogs": product_blogs_serialized.data}, status=status.HTTP_200_OK
    )
