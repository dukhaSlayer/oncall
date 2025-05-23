from django.db import models

from apps.alerts.models import AlertGroup
from apps.mattermost.client import MattermostPost


class MattermostMessage(models.Model):
    (
        ALERT_GROUP_MESSAGE,
        LOG_MESSAGE,
    ) = range(2)

    MATTERMOST_MESSAGE_CHOICES = (
        (ALERT_GROUP_MESSAGE, "Alert group message"),
        (LOG_MESSAGE, "Log message"),
    )

    post_id = models.CharField(max_length=100)

    channel_id = models.CharField(max_length=100)

    message_type = models.IntegerField(choices=MATTERMOST_MESSAGE_CHOICES)

    alert_group = models.ForeignKey(
        "alerts.AlertGroup",
        on_delete=models.CASCADE,
        related_name="mattermost_messages",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["alert_group", "message_type", "channel_id"],
                name="unique_alert_group_message_type_channel_id",
            )
        ]

        indexes = [
            models.Index(fields=["channel_id", "post_id"]),
        ]

    @staticmethod
    def create_message(alert_group: AlertGroup, post: MattermostPost, message_type: int):
        return MattermostMessage.objects.create(
            alert_group=alert_group, post_id=post.post_id, channel_id=post.channel_id, message_type=message_type
        )
