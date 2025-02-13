from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product, Industry
from .serializers import (
    ProductSerializerShow,
    ProductSerializerFull,
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

    # Checking if both 'product_type' and 'industry' are provided
    if product_type and industry:
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
            products_list = Product.objects.filter(
                product_type=product_type, industry=industry
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
