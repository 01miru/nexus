from django.contrib.auth.models import User
from django.db import models


class ProcessKillHistory(models.Model):
    process_name = models.CharField(max_length=255)
    pid = models.IntegerField()
    killed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    kill_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.process_name} (PID: {self.pid}) killed at {self.kill_time}"
