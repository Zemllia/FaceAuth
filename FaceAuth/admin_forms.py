from django import forms

from FaceAuth.models import Visitor


class VisitorForm(forms.ModelForm):

    class Meta:
        model = Visitor
        fields = (
            'first_name',
            'last_name',
            'patronymic',
            'access_level',
            'face_image'
        )
