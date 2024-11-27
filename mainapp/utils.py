from django.contrib.auth.models import Users

def create_user_with_default_password(username, email):
    user = Users.objects.create_user(username=username, email=email)
    default_password = "password123"  # Contraseña predeterminada
    user.set_password(default_password)
    user.save()
    return user