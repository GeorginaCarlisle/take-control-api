import os
from rest_framework import serializers
from datetime import datetime, timezone
from .models import Task
from focus.models import Focus
from goals.models import Goal


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model. It changes owner.id into owner.username,
    and adds extra fields is_owner, deadline_near, goal_deadline_near, focus_image
    and goal_name
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    deadline_near = serializers.SerializerMethodField()
    goal_deadline_near = serializers.SerializerMethodField()
    goal_name = serializers.SerializerMethodField()
    active = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner
    
    def get_deadline_near(self, obj):
        """
        Generates a new field containing information if the deadline is less than 2 days away
        """
        future_deadline = obj.deadline
        if future_deadline:
            today_naive = datetime.now()
            today_aware = today_naive.replace(tzinfo=timezone.utc)
            days_remaining = (future_deadline - today_aware).days
            if days_remaining == 0:
                return "Due Today!!"
            elif days_remaining == 1:
                return "Due Tomorrow!!"
            else:
                return None
        else:
            return None

    def get_goal_deadline_near(self, obj):
        """
        Generates a new field containing information if the linked goal is near
        """
        if obj.goal:
            goal_id = obj.goal.id
            goal = Goal.objects.get(id=goal_id)
            goal_deadline = goal.deadline
            if goal_deadline:
                today_naive = datetime.now()
                today_aware = today_naive.replace(tzinfo=timezone.utc)
                days_remaining = (goal_deadline - today_aware).days
                easy_date = goal_deadline.strftime('%d/%m/%y')
                if days_remaining<=7:
                    return f'Goal due on the {easy_date} only {days_remaining} days to go'
                else:
                    return f'Goal due on the {easy_date}'
            else:
                return None
        else:
            return None

    def get_goal_name(self, obj):
        """
        Generates a new field containing the name of the linked goal,
        if no goal but a focus handles
        if no goal and no focus handles
        """
        if obj.goal:
            goal_id = obj.goal.id
            goal = Goal.objects.get(id=goal_id)
            return goal.title
        else:
            if obj.focus:
                return "Day-to-day"
            else:
                return "Miscellaneous"

    def get_active(self,obj):
        """
        generates a new field that is true if no goal, or goal is active
        and false if goal is not active
        """
        if obj.goal:
            goal_id = obj.goal.id
            goal = Goal.objects.get(id=goal_id)
            if goal.active:
                return True
            else:
                return False
        else:
            return True

    class Meta:
        model = Task
        fields = [
            'id',
            'owner',
            'is_owner',
            'created_at',
            'updated_at',
            'focus',
            'goal',
            'today',
            'achieved',
            'name',
            'deadline',
            'labels',
            'deadline_near',
            'goal_deadline_near',
            'goal_name',
            'active'
        ]