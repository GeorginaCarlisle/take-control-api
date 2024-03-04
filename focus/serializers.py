from rest_framework import serializers
from .models import Focus

class FocusSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()

    def validate_image(self, value):
        """
        A custom validation method for the image field.
        This code has been copied from the Django rest walkthrough
        """
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'Image size larger than 2MB!'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width larger than 4096px'
            )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height larger tahn 4096px'
            )
        return value


    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner