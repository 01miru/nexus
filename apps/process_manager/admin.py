from django.contrib import admin
from process_manager.models import Snapshot, SnapshotProcess


class SnapshotProcessInline(admin.TabularInline):
    model = SnapshotProcess
    extra = 0


@admin.register(Snapshot)
class SnapshotAdmin(admin.ModelAdmin):
    list_display = ("created_at", "created_by")
    search_fields = ("created_by__username",)
    inlines = [SnapshotProcessInline]
