from allauth.account.utils import user_email
from django import forms
from .models import Post
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=20)
    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'author',
            'category',
        ]

        def clean(self):
            cleaned_data = super().clean()
            text = cleaned_data.get("text")
            title = cleaned_data.get("title")

            if title == text:
                raise ValidationError(
                    "Описание не должно быть идентично названию."
                )

            return cleaned_data


class CommonSignupForm(SignupForm):

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user

