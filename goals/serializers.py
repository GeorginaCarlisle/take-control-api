from rest_framework import serializers
from datetime import datetime, timedelta
from .models import Goal


class GoalSerializer(serializers.ModelSerializer):
    """
    Serializer for the Goal model. It changes owner.id into owner.username,
    adds an extra field is_owner .....
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    days_remaining = serializers.SerializerMethodField()
    deadline_near = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_days_remaining(self, deadline):
        """
        Generates a new field containing the number of days remaining until
        the deadline.
        """
        if deadline:
            today = timedelta(datetime.now())
            future_deadline = timedelta(deadline)
            time_difference = future_deadline - today
            days_remaining = time_difference.day
            return days_remaining
        else:
            return None

    def get_deadline_near(self, obj):
        """
        Generates a new field that is either true if the deadline is less
        than 7 days, or false if their is no deadline or the deadline is
        more than 7 days away.
        """
        days_remaining = self.get_days_remaining(obj)
        if days_remaining:
            if days_remaining <= 7:
                return True
            else:
                return False
        else:
            return False

    class Meta:
        model = Goal
        fields = [
            'id',
            'owner',
            'is_owner',
            'focus',
            'children',
            'parent',
            'created_at',
            'updated_at',
            'active',
            'deadline',
            'title',
            'description',
            'value',
            'criteria',
            'deadline_near',
            'days_remaining'
        ]
