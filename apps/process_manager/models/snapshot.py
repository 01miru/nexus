from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


class Snapshot(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Snapshot"
        verbose_name_plural = "Snapshots"
        ordering = ["-created_at"]

    @property
    def get_processes_count(self) -> int:
        return self.processes.count()

    @property
    def get_total_memory(self) -> float:
        return round(
            (
                self.processes.aggregate(total_memory=Sum("memory"))["total_memory"]
                or 0.0
            ),
            2,
        )

    @property
    def get_total_cpu(self) -> float:
        return round(
            self.processes.aggregate(total_cpu=Sum("cpu"))["total_cpu"] or 0.0, 2
        )


class SnapshotProcess(models.Model):
    snapshot = models.ForeignKey(
        Snapshot, on_delete=models.CASCADE, related_name="processes"
    )
    pid = models.IntegerField()
    name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    duration = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    cpu = models.FloatField()
    memory = models.FloatField()

    class Meta:
        verbose_name = "Snapshot Process"
        verbose_name_plural = "Snapshot Processes"
        ordering = ["-snapshot__created_at"]
