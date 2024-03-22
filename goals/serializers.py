from rest_framework import serializers
from datetime import datetime, timezone
from .models import Goal


class GoalSerializer(serializers.ModelSerializer):
    """
    Serializer for the Goal model. It changes owner.id into owner.username,
    adds extra fields is_owner, days_remaining and deadline_near
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    days_remaining = serializers.SerializerMethodField()
    deadline_near = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_days_remaining(self, obj):
        """
        Generates a new field containing the number of days remaining until
        the deadline.
        """
        future_deadline = obj.deadline
        if future_deadline:
            today_naive = datetime.now()
            today_aware = today_naive.replace(tzinfo=timezone.utc)
            days_remaining = (future_deadline - today_aware).days
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
        if days_remaining is not None:
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
