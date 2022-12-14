from django.contrib import admin
from lastSeenRP.models import rpCharacter, Appearance
# Register your models here.
#admin.site.register(rpCharacter)
#admin.site.register(Appearance)

#shows appearances under a character in the admin menu if they need to be created there
class AppearanceInline(admin.TabularInline):
    model = Appearance
    #only one extra one
    extra = 1

class rpCharacterAdmin(admin.ModelAdmin):
    #fields that are displayed in the admin panel
    fields = [ 'character_first_name','character_nick_name', 'character_last_name', 'character_played_by', 'character_image', 'streamers_URL']
    #
    list_display = ('character_first_name','character_nick_name', 'character_last_name', 'character_played_by', 'character_image', 'streamers_URL')
    inlines = [AppearanceInline]
    #fields that will appear in the results of a search
    search_fields = ['character_first_name','character_nick_name', 'character_last_name', 'character_played_by', 'streamers_URL']

class AppearanceAdmin(admin.ModelAdmin):
    #fields = ['character_name', 'date_of_appearance', 'twitch_clip_URL', 'clip_Streamer', 'publish_time']
    fieldsets = [
        (None, {'fields': ['character_name', 'date_of_appearance']}),
        ('Additional Info', {'fields': ['twitch_clip_URL', 'clip_Streamer', 'publish_time', 'submittedBy']}),
    ]
    list_display = ('character_name', 'date_of_appearance', 'twitch_clip_URL', 'clip_Streamer', 'publish_time', 'recently_published', 'recently_appeared', 'submittedBy')
    list_filter= ['date_of_appearance']
    search_fields = ['character_name']



#objects that will appear in the admin site
admin.site.register(rpCharacter, rpCharacterAdmin)
admin.site.register(Appearance, AppearanceAdmin)