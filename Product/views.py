from decimal import Decimal

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from uuid import UUID
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Product, ProductImage, MainImage, ProductColor, TypeOfFile, Industry
from AuthenticationSystem.models import CustomUser
from .serializers import (
    ProductSerializerFull,
    ProductSerializerShow,
    IndustrySerializer,
)


@api_view(["GET"])
def industries_list_show(request):
    """
    Retrieves and returns the list of all industries.
    Returns a JSON response with the industry list.
    """
    industies_list = Industry.objects.all()
    serialized_data = IndustrySerializer(industies_list, many=True)

    # Returns the serialized data of all industries with a status code 200 (OK)
    return Response({"industries": serialized_data.data}, status=200)


@api_view(["GET"])
def products_sort_show(request):
    """
    Retrieves and returns a list of products filtered by product_type and industry.
    The query parameters 'product_type' and 'industry' are required.
    Returns a JSON response with the filtered list of products.
    """
    # Extracting the 'product_type' and 'industry' from the query parameters
    product_type = request.query_params.get("product_type")
    industry = request.query_params.get("industry")
    title = request.query_params.get("title")

    if all([product_type, industry, title]):
        if str(product_type).lower() == "physical":
            # Filtering physical products by 'product_type' and 'industry'
            products_list = Product.objects.filter(
                product_type=product_type,
                industry=industry,
                title__icontains=title,
                active=True,
            )
            # Serializing the list of products and returning it in the response
            serialized_data = ProductSerializerShow(products_list, many=True)
            return Response({"products": serialized_data.data}, status=200)

        elif str(product_type).lower() == "digital":
            # Filtering digital products by 'product_type' and 'industry'
            type_of_file = request.query_params.get("type_of_file")

            products_list = Product.objects.filter(
                product_type=product_type,
                industry=industry,
                type_of_file=type_of_file,
                title__icontains=title,
            )
            # Serializing the list of products and returning it in the response
            serialized_data = ProductSerializerShow(products_list, many=True)
            return Response({"products": serialized_data.data}, status=200)

        # If the product_type is neither 'physical' nor 'digital'
        else:
            return Response(
                {
                    "error": "Invalid 'product_type' provided. Must be 'Physical' or 'Digital'."
                },
                status=400,
            )

    # Checking if both 'product_type' and 'industry' are provided
    elif product_type and industry:
        # Handling different types of products based on 'product_type'
        if str(product_type).lower() == "physical":
            # Filtering physical products by 'product_type' and 'industry'
            products_list = Product.objects.filter(
                product_type=product_type, industry=industry
            )
            # Serializing the list of products and returning it in the response
            serialized_data = ProductSerializerShow(products_list, many=True)
            return Response({"products": serialized_data.data}, status=200)

        elif str(product_type).lower() == "digital":
            # Filtering digital products by 'product_type' and 'industry'
            type_of_file = request.query_params.get("type_of_file")

            products_list = Product.objects.filter(
                product_type=product_type,
                industry=industry,
                type_of_file=type_of_file,
            )
            # Serializing the list of products and returning it in the response
            serialized_data = ProductSerializerShow(products_list, many=True)
            return Response({"products": serialized_data.data}, status=200)

        # If the product_type is neither 'physical' nor 'digital'
        else:
            return Response(
                {
                    "error": "Invalid 'product_type' provided. Must be 'Physical' or 'Digital'."
                },
                status=400,
            )
    else:
        # If any of the required parameters ('product_type' or 'industry') are missing
        return Response(
            {"error": "'product_type' and 'industry' are required parameters."},
            status=400,
        )


@api_view(["GET"])  # Defines a GET API endpoint
def product_detail(request):
    product_id = request.query_params.get(
        "product_id"
    )  # Retrieves product_id from query parameters

    if product_id:
        product_detail = Product.objects.filter(
            id=product_id
        ).first()  # Fetches the product by ID
        if product_detail:
            product_detail_serialized = ProductSerializerFull(
                product_detail
            )  # Serializes product data
            return Response(
                {"product_detail": product_detail_serialized.data}, status=200
            )  # Returns product details
        else:
            return Response(
                {"error": "Product not found"}, status=404
            )  # Returns error if product does not exist

    return Response(
        {"error": "product_id is required"}, status=400
    )  # Returns error if product_id is missing


def get_user_from_token(request):
    token = request.headers.get("Authorization")
    if not token:
        return None, Response(
            {"error": "Authentication token is required"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    token = str(token).replace("Bearer ", "")
    try:
        validated_token = JWTAuthentication().get_validated_token(token)
        user = JWTAuthentication().get_user(validated_token)
        return user, None
    except Exception as e:
        return None, Response(
            {"error": "Invalid or expired token"}, status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def create_product(request):
    # Extract user from token
    user, error_response = get_user_from_token(request)

    if error_response:
        return error_response
    # Ensure only store owners can create products
    if user.user_type != "store_owner":
        return Response(
            {"error": "Only store owners can create products"},
            status=status.HTTP_403_FORBIDDEN,
        )

    # Retrieve data from request
    data = request.data
    user_owner = user
    product_title = data.get("product_title")
    product_price = Decimal(data.get("product_price", "0"))
    description = data.get("description", "")
    product_type = data.get("product_type")
    length = data.get("length")
    width = data.get("width")
    color_name = data.get("color")
    size = data.get("size")
    type_of_file = data.get("type_of_file")

    # Validate required fields
    if not all([product_title, product_price, product_type]):
        return Response(
            {"error": "product_title, product_price, and product_type are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    product_type = product_type.capitalize()

    if product_type == "Physical":
        # Validate required fields for physical products
        if not all([description, length, width, color]):
            return Response(
                {
                    "error": "description, length, width, color are required for physical products"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Ensure the color exists in the database
        try:
            color = ProductColor.objects.get(name=color_name)
        except ProductColor.DoesNotExist:
            return Response(
                {"error": "Invalid color"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create physical product
        product = Product.create_physical(
            title=product_title,
            price=product_price,
            store_owner=user_owner,
            descriptions=description,
            length=length,
            width=width,
            color=color,
        )

    elif product_type == "Digital":
        # Validate required fields for digital products
        if not all([size, type_of_file]):
            return Response(
                {"error": "size and type_of_file are required for digital products"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Ensure the file type exists in the database
        try:
            type_of_file = TypeOfFile.objects.get(name_of_type=type_of_file)
        except TypeOfFile.DoesNotExist:
            return Response(
                {"error": "Invalid file type"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create digital product
        product = Product.create_digital(
            title=product_title,
            price=product_price,
            descriptions=description,
            size=size,
            type_of_file=type_of_file,
        )

    else:
        return Response(
            {"error": "Invalid product type"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Handle image uploads
    images = request.FILES.getlist("images")
    if not images:
        return Response(
            {"error": "At least one image is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Save the first image and set it as the main image
    first_image = ProductImage.objects.create(product=product, image=images[0])
    MainImage.objects.create(product=product, product_image=first_image)

    # Save the rest of the uploaded images (excluding the first one)
    for image in images[1:]:
        ProductImage.objects.create(product=product, image=image)

    return Response(ProductSerializerFull(product).data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def show_products_by_store(request):
    """
    API endpoint to retrieve all products of a specific store owner.
    Only users with user_type='store_owner' are considered valid store owners.
    """
    store_owner_id = request.query_params.get(
        "store_owner_id"
    )  # Retrieve store_owner_id from query parameters

    if not store_owner_id:
        return Response({"error": "store_owner_id is required."}, status=400)

    store_owner = CustomUser.objects.filter(
        id=store_owner_id, user_type="store_owner"
    ).first()

    if not store_owner:
        return Response(
            {"error": "No store owner found with the given ID."}, status=404
        )

    user = get_user_from_token(request)
    if (user.user_type == "store_owner") and (user.id == UUID(store_owner_id)):
        products_list = store_owner.products.all()

    else:
        products_list = store_owner.products.filter(active=True)

    if not products_list.exists():
        return Response(
            {"error": "No products found for this store owner."}, status=404
        )

    serialized_products = ProductSerializerShow(products_list, many=True)
    return Response({"products": serialized_products.data}, status=200)


@api_view(["DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def delete_product(request):
    # Get the user from the token
    user, error_response = get_user_from_token(request)

    # If there is an error with authentication, return the error response
    if error_response:
        return error_response

    # Check if the user's type is either 'store_owner' or 'admin'
    if (user.user_type != "store_owner") and (user.user_type != "admin"):
        return Response(
            {"error": "Your user_type isn't suitable"},
            status=status.HTTP_403_FORBIDDEN,
        )

    # Get the product_id from the query parameters
    request_data = request.query_params
    product_id = request_data.get("product_id")

    # Retrieve the product by its UUID
    target_product = Product.objects.filter(id=UUID(product_id)).first()

    # Delete the product from the database
    target_product.delete()

    # Return a successful response after deleting the product
    return Response({"product deleted"}, status=status.HTTP_200_OK)
