from django.db import models


class MattermostUser(models.Model):
    user = models.OneToOneField(
        "user_management.User", on_delete=models.CASCADE, related_name="mattermost_user_identity"
    )
    mattermost_user_id = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100, null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["mattermost_user_id"]),
        ]

    @property
    def mention_username(self):
        return f"@{self.username}"
