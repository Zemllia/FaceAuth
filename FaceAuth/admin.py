import base64
import pickle

from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe

from FaceAuth import utils
from FaceAuth.admin_forms import VisitorForm
from FaceAuth.models import AccessLevel, Visitor, Camera, CameraLog


class VisitorAdmin(admin.ModelAdmin):

    form = VisitorForm

    list_display = (
        'last_name',
        'first_name',
        'patronymic',
        'access_level'
    )
    list_filter = (
        'access_level',
    )
    search_fields = (
        'last_name',
        'first_name',
        'patronymic'
    )

    def save_model(self, request, obj, form, change):
        obj.face_image_vectors = None
        obj.save()
        obj.face_image_vectors = utils.vector2bytes(utils.image2vector("FaceAuth/" + obj.face_image.url))
        obj.save()


class CameraAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'need_access_level',
    )
    list_filter = (
        'need_access_level',
    )
    search_fields = (
        'name',
    )


class CameraLogAdmin(admin.ModelAdmin):

    readonly_fields = ["camera", "success", "date", "image"]

    def has_add_permission(self, request):
        return False

    search_fields = (
        'date',
    )


admin.site.register(Camera, CameraAdmin)
admin.site.register(AccessLevel)
admin.site.register(CameraLog, CameraLogAdmin)
admin.site.register(Visitor, VisitorAdmin)
