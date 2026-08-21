# users/tokens.py

from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    # Add custom claims to the token
    refresh['username'] = user.username
    refresh['role'] = user.role
    refresh['user_id'] = user.id
    refresh['email'] = user.email

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
