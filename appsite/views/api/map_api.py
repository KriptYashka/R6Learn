from rest_framework.response import Response
from rest_framework.views import APIView

from appsite.models import MapModel
from appsite.serializers import MapSerializer


class GetMapInfoView(APIView):
    def get(self, request):
        queryset = MapModel.objects.all()
        serializer_for_queryset = MapSerializer(
            instance=queryset,
            many=True
        )
        return Response(serializer_for_queryset.data)