from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.files.images import get_image_dimensions
from .models import CustomUser, UserProfile


class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(required=True, help_text="Enter your phone number")
    photo = forms.ImageField(required=False, help_text="Upload a profile picture")

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'password1', 'password2', 'phone_number', 'photo')

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            w, h = get_image_dimensions(photo)
            if w > 300:
                raise forms.ValidationError("The image is too wide")
            if h > 300:
                raise forms.ValidationError("The image is too tall")
        return photo

    def save(self, commit=True):
        user = super().save(commit=False)
        user.phone_number = self.cleaned_data['phone_number']
        if commit:
            user.save()
            if self.cleaned_data.get('photo'):
                UserProfile.objects.create(user=user, photo=self.cleaned_data['photo'])
        return user


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password')