import os
from rest_framework import serializers
from datetime import datetime, timezone, date, timedelta
from .models import Task
from focus.models import Focus
from goals.models import Goal


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model. It changes owner.id into owner.username,
    and adds extra fields is_owner, deadline_near, goal_deadline_near,
    focus_image and goal_name
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
        Generates a new field containing information if the deadline is
        less than 2 days away
        """
        future_deadline = obj.deadline
        if future_deadline:
            today_naive = datetime.now()
            today_aware = today_naive.replace(tzinfo=timezone.utc)
            days_remaining = (future_deadline - today_aware).days
            easy_date = future_deadline.strftime('%d/%m/%y')
            if days_remaining < -1:
                return f'Task OVERDUE!! {easy_date}'
            elif days_remaining < 3:
                today = date.today()
                today_day = today.day
                deadline_day = future_deadline.day
                if today_day == deadline_day:
                    return f'due TODAY {easy_date}'
                tomorrow = today + timedelta(days=1)
                tomorrow_day = tomorrow.day
                if deadline_day == tomorrow_day:
                    return f'due tomorrow {easy_date}'
                else:
                    return f'due {easy_date}'
            else:
                return f'due {easy_date}'
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

                if days_remaining < -1:
                    return f'GOAL OVERDUE!! {easy_date}'
                elif days_remaining < 3:
                    today = date.today()
                    today_day = today.day
                    deadline_day = goal_deadline.day
                    if today_day == deadline_day:
                        return f'Goal due TODAY {easy_date}'
                    tomorrow = today + timedelta(days=1)
                    tomorrow_day = tomorrow.day
                    if deadline_day == tomorrow_day:
                        return f'Goal due TOMORROW {easy_date}'
                    else:
                        return f'Goal due {easy_date}'
                else:
                    return f'Goal due {easy_date}'
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
            return f'A step towards {goal.title}'
        else:
            if obj.focus:
                return f'A day-to-day {obj.focus.name} task'
            else:
                return "A miscellaneous task"

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
            'context',
            'image'
        ]
