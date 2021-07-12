from rest_framework import serializers

from .models import Host, HostImage, HostComment, HostAddress


class HostelImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = HostImage
        fields =["img"]


class HostelCommentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = HostComment
        fields = "__all__"


class HostelAddressSerializers(serializers.ModelSerializer):
    state = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = HostAddress
        exclude = ["id", "host"]


class HostListSerializer(serializers.HyperlinkedModelSerializer):
    # host_address = HostelAddressSerializers(read_only=True)
    owner = serializers.StringRelatedField(read_only=True)
    host_address = serializers.StringRelatedField(read_only=True)
    cat = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Host
        fields = "__all__"
        # lookup_field = 'slug'
        # extra_kwargs = {'detail': {'lookup_field': 'slug'}}


class HostDetailSerializer(serializers.ModelSerializer):
    host_address = HostelAddressSerializers(read_only=True)
    host_comments = HostelCommentsSerializers(many=True, read_only=True)
    host_image = HostelImageSerializers(many=True)
    owner = serializers.StringRelatedField(read_only=True)
    cat = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Host
        exclude = ["id"]

