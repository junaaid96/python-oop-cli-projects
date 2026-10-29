from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Project, Proposal, Skill, User


@admin.register(User)
class HubUserAdmin(UserAdmin[User]):
    list_display = ("username", "email", "role", "is_staff")
    list_filter = ("role", "is_staff")
    fieldsets = (*(UserAdmin.fieldsets or ()), ("Marketplace", {"fields": ("role",)}))


class ProposalInline(admin.TabularInline[Proposal, Project]):
    model = Proposal
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin[Project]):
    list_display = ("title", "client", "budget", "status", "created_at")
    list_filter = ("status", "skills")
    search_fields = ("title", "description")
    list_select_related = ("client",)  # avoid N+1 on the change list
    inlines = (ProposalInline,)


admin.site.register(Skill)
