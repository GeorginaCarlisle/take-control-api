from rest_framework import serializers
from .models import Focus


class FocusSerializer(serializers.ModelSerializer):
    """
    Serializer for the Focus model. It changes owner.id into owner.username,
    adds an extra field is_owner, prevents large images being saved to the
    database and changes date fields into an easier format
    """
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

    class Meta:
        model = Focus
        fields = [
            'id',
            'owner',
            'created_at',
            'updated_at',
            'name',
            'rank',
            'why',
            'image',
            'is_owner'
        ]
