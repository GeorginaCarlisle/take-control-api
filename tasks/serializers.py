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
    deadline_info = serializers.SerializerMethodField()
    goal_deadline_info = serializers.SerializerMethodField()
    context = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner
    
    def get_deadline_info(self, obj):
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
                easy_date = future_deadline.strftime('%d/%m/%y')
                return f'Due {easy_date}'
        else:
            return None

    def get_goal_deadline_info(self, obj):
        """
        Generates a new field containing information if the linked goal is near
        """
        if obj.goal:
            if obj.goal.deadline:
                goal_deadline = obj.goal.deadline
                today_naive = datetime.now()
                today_aware = today_naive.replace(tzinfo=timezone.utc)
                days_remaining = (goal_deadline - today_aware).days
                easy_date = goal_deadline.strftime('%d/%m/%y')
                if days_remaining<=7:
                    return f'due on the {easy_date} only {days_remaining} days to go'
                else:
                    return f'due on the {easy_date}'
            else:
                return None
        else:
            return None

    def get_context(self, obj):
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
                return f'Day-to-day {obj.focus.name} task'
            else:
                return "Miscellaneous task"


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
            'active',
            'deadline_info',
            'goal_deadline_info',            
            'context'
        ]
