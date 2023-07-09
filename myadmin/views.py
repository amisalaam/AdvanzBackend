from django.shortcuts import render
from django.contrib.auth import get_user_model

# Create your views here.

def admin_create_doctor(email, name, password):
    User = get_user_model()
    try:
        user = User.objects.create_doctor(email=email, name=name, password=password)
        print("Doctor created successfully.")
        print(f"Email: {user.email}")
        print(f"Name: {user.name}")
        return user
    except ValueError as e:
        print(str(e))
        return None
    



