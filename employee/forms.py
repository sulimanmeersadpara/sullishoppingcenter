from accounts.models import User 
from django import forms


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_image']