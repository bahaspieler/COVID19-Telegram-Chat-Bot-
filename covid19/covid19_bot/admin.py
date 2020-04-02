from django.contrib import admin
from .models import first_button, bot_user, country_update
from import_export import resources

class BotUserResource(resources.ModelResource):
    class Meta:
        model = bot_user

class BotUserAdmin(admin.ModelAdmin):
    list_display= ('user_name', 'user_id', 'query', 'country_notif', 'date_country')
    list_filter= ('user_name', 'user_id', 'query', 'country_notif', 'date_country')
    resource_class = BotUserResource

admin.site.register(first_button)
admin.site.register(bot_user, BotUserAdmin)
admin.site.register(country_update)