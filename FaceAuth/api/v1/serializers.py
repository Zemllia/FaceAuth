from rest_framework import serializers


class CheckImageSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True)

    class Meta:
        ref_name = 'CheckImage'
