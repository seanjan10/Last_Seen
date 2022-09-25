from django.contrib import admin
from lastSeenRP.models import rpCharacter, Appearance
# Register your models here.
#admin.site.register(rpCharacter)
#admin.site.register(Appearance)

class AppearanceInline(admin.TabularInline):
    model = Appearance
    extra = 1

class rpCharacterAdmin(admin.ModelAdmin):
    fields = [ 'character_first_name','character_nick_name', 'character_last_name', 'character_played_by', 'streamers_URL']
    list_display = ('character_first_name','character_nick_name', 'character_last_name', 'character_played_by', 'streamers_URL')
    inlines = [AppearanceInline]
    search_fields = ['character_first_name','character_nick_name', 'character_last_name', 'character_played_by', 'streamers_URL']

class AppearanceAdmin(admin.ModelAdmin):
    #fields = ['character_name', 'date_of_appearance', 'twitch_clip_URL', 'clip_Streamer', 'publish_time']
    fieldsets = [
        (None, {'fields': ['character_name', 'date_of_appearance']}),
        ('Additional Info', {'fields': ['twitch_clip_URL', 'clip_Streamer', 'publish_time']}),
    ]
    list_display = ('character_name', 'date_of_appearance', 'twitch_clip_URL', 'clip_Streamer', 'publish_time', 'recently_published')
    list_filter= ['date_of_appearance']
    search_fields = ['character_name']




admin.site.register(rpCharacter, rpCharacterAdmin)
admin.site.register(Appearance, AppearanceAdmin)