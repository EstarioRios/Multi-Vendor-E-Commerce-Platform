from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import CustomUserSerializer_Full
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes


# Function to generate JWT tokens (access and refresh) for a given user
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user=user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


@api_view(["POST"])
def signup(request):
    # Extracting user details from request data
    username = request.data.get("username")
    password = request.data.get("password")
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")
    store_name = request.data.get("store_name")
    industry = request.data.get("industry")
    user_type = request.data.get("user_type")

    # Checking if user_type is provided
    if user_type is None:
        return Response({"error": "user_type is required"}, status=400)

    # Handling customer registration
    if user_type == "customer":
        # Ensuring all required fields are provided
        if not all([username, password, first_name, last_name]):
            return Response({"error": "All fields are required"}, status=400)

        try:
            # Creating a new customer user
            user = CustomUser.objects.create_customer(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            # Generating JWT tokens for the newly created user
            tokens = get_tokens_for_user(user=user)
            return Response(
                {
                    "success": "Customer created successfully",
                    "tokens": tokens,
                    "user": CustomUserSerializer_Full(user).data,
                },
                status=201,
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

    # Handling store owner registration
    elif user_type == "store_owner":
        # Ensuring all required fields are provided
        if not all(
            [
                username,
                password,
                first_name,
                last_name,
                industry,
                store_name,
            ]
        ):
            return Response({"error": "All fields are required"}, status=400)

        try:
            # Creating a new store owner user
            user = CustomUser.objects.create_store_owner(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                industry=industry,
                store_name=store_name,
            )
            # Generating JWT tokens for the newly created user
            tokens = get_tokens_for_user(user=user)
            user_info = (
                CustomUser.objects.filter(id=user.id)
                .values(
                    "first_name",
                    "last_name",
                    "id",
                    "user_type",
                )
                .first()
            )
            return Response(
                {
                    "success": "Store owner created successfully",
                    "tokens": tokens,
                    "user": user_info,
                },
                status=201,
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

    # Returning an error response for an invalid user type
    return Response({"error": "Invalid user type"}, status=400)


@api_view(["POST"])
def login_manual(request):
    # Get user credentials
    username = request.data.get("username")
    password = request.data.get("password")

    # Check for missing fields
    if any(field is None for field in [username, password]):
        return Response({"error": "All fields are required"}, status=400)

    # Authenticate user
    user = authenticate(username=username, password=password)
    if user is None:
        return Response({"error": "user is not exist"}, status=401)

    # Generate tokens for user
    tokens = get_tokens_for_user(user=user)
    user_info = (
        CustomUser.objects.filter(id=user.id)
        .values(
            "first_name",
            "last_name",
            "id",
            "user_type",
        )
        .first()
    )

    # Return success response with tokens and user data
    return Response(
        {
            "success": "Login was successful",
            "tokens": tokens,
            "user": user_info,
        }
    )


@api_view(["POST"])
def login_JWT(request):
    # Get token from header
    token = request.headers.get("Authorization")

    # If no token, return 401
    if token is None:
        return Response({"value": False}, status=401)

    # Clean token
    token = str(token).replace("Bearer ", "")

    try:
        # Validate token and get user
        validated_token = JWTAuthentication().get_validated_token(token)
        user = JWTAuthentication().get_user(validated_token)
    except AuthenticationFailed:
        return Response({"value": False}, status=401)

    # Return success if user is valid
    return Response({"value": True}, status=200)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_information(request):
    user = request.user
    user_data = CustomUserSerializer_Full(user).data
    return Response({"user_data": user_data})
