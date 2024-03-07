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
    focus_image = serializers.SerializerMethodField()
    goal_name = serializers.SerializerMethodField()

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
        goal_id = obj.goal
        if goal_id:
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

    def get_focus_image(self, obj):
        """
        Generates a new field containing the image for the connected focus,
        if no connected focus adds the miscellaneous image
        """
        focus_id = obj.focus
        if focus_id:
            focus = Focus.objects.get(id=focus_id)
            return focus.image
        else:
            cloudinary_url = os.environ.get('CLOUDINARY_URL')
            return f'{cloudinary_url}/miscellaneous-tasks_b6f2gl'

    def get_goal_name(self, obj):
        """
        Generates a new field containing the name of the linked goal,
        if no goal but a focus handles
        if no goal and no focus handles
        """
        goal_id = obj.goal
        if goal_id:
            goal = Goal.objects.get(id=goal_id)
            return goal.name
        else:
            focus_id = obj.focus
            if focus_id:
                return "Day-to-day"
            else:
                return "Miscellaneous"

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
            'focus_image',
            'goal_name'
        ]