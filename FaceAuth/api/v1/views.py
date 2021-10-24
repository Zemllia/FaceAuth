import os

from django.core.files.base import ContentFile
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from drf_yasg.inspectors import SwaggerAutoSchema
from rest_framework.response import Response
from django.core.files.storage import default_storage

from FaceAuth import utils, settings
from FaceAuth.api.v1.serializers import CheckImageSerializer
from FaceAuth.models import Visitor, CameraLog

check_image_schema = swagger_auto_schema(
    auto_schema=SwaggerAutoSchema,
    tags=['api'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['member_id', 'fight_session_id'],
        properties={
            'image': openapi.Schema(type=openapi.TYPE_FILE)
        }
    ),
    operation_id="Проверить лицо на фотографии"
)


class CheckImageView(APIView):
    @check_image_schema
    def post(self, request):
        serializer = CheckImageSerializer(data=request.data)
        request_camera = request.camera
        print(request_camera)
        if serializer.is_valid():
            data = serializer.validated_data
            img_extension = str(data.get("image").name).split('.')[-1]
            tmp_file_name = utils.generate_file_name() + "." + img_extension
            image_path = f"tmp/{tmp_file_name}"
            default_storage.save(image_path, ContentFile(data.get("image").read()))
            check_face_vector = utils.image2vector(settings.MEDIA_ROOT + "/" + image_path)
            if check_face_vector is None:
                answer = {"message": "face not recognized"}
                return Response(status=status.HTTP_400_BAD_REQUEST, data=answer)
            all_visitors = Visitor.objects.all()
            known_ids = []
            known_face_encodings = []
            for visitor in all_visitors:
                known_ids.append(visitor.id)
                known_face_encodings.append(utils.bytes2vector(visitor.face_image_vectors))
            compare_result = utils.compare_images(known_face_encodings, check_face_vector)
            os.remove(settings.MEDIA_ROOT + "/" + image_path)
            granted_visitor = None
            for i in range(0, len(compare_result)):
                print(i)
                if compare_result[i]:
                    granted_visitor = Visitor.objects.get(id=known_ids[i])
                    break
            print(granted_visitor)
            if granted_visitor and granted_visitor.access_level.level >= request_camera.need_access_level.level:
                answer = {"message": "granted"}
                new_log_write = CameraLog(camera=request_camera, success=True, image=data.get("image"))
                new_log_write.save()
                return Response(status=status.HTTP_200_OK, data=answer)
            answer = {"message": "not granted"}
            new_log_write = CameraLog(camera=request_camera, success=False, image=data.get("image"))
            new_log_write.save()
            return Response(status=status.HTTP_200_OK, data=answer)
        else:
            answer = serializer.errors
            return Response(status=status.HTTP_400_BAD_REQUEST, data=answer)


class GetCameraName(APIView):
    def get(self, request):
        answer = {"message": "success", "data": {"name": request.camera.name}}
        return Response(status=status.HTTP_200_OK, data=answer)
