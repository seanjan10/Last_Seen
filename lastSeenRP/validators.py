from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import pytz
import re

def valid_ascii_character(value, isNickName):
    if isNickName == True:
        #blackListChars = [',', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '=', '+', '[', ']', '{', '}', '|', '\\', ':', ';', '~', '`', '?', '/' , '<', '>']
        pattern = "([A-Za-z0-9\-\'\.\_\"])+"
    else:
        #blackListChars = [',', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '=', '+', '[', ']', '{', '}', '|', '\\', ':', ';', '~', '`', '?', '/' , '<', '>', '\"']
        pattern = "([A-Za-z0-9\-\'\.\_])+"

    x = re.fullmatch(pattern, value)
    if x == None:
        return False
    else: 
        return True


    '''
    if any(ch in blackListChars for ch in value):
        return False
    else:
        return True
    '''

def validate_channel_name(value):
    #twitch username constraints
    pattern = "^([a-zA-Z0-9][a-zA-Z0-9_]{3,25})$"
    x = re.fullmatch(pattern, value)

    if x == None:
        raise ValidationError(
            _("Channel names can only be alphanumeric including underscores (cannot start with an underscore) and must have more than 3 characters")
    )

    return value

def validate_character_nick_name(value):

    if valid_ascii_character(value, True) == False:
        raise ValidationError(
            _("Names can only include alphanumerical characters as well as (\" - \", \" ' \", \" . \", \" _ \", for nick names quotation marks (\") are also allowed)")
    )
    if value.startswith('\"') and value.endswith('\"'):
            return value
    else:
        raise ValidationError(
            _("Nick names should be enclosed with quotation marks. (\"\")")
        )

def validate_character_last_name(value):
    if " " in value:
        raise ValidationError(
            _("Last names cannot include spaces. Instead use underscores( _ ). Additional Characters that are allowed are (-, ', .)")
        )
    if valid_ascii_character(value, False) == False:
        raise ValidationError(
            _("Names can only include alphanumerical characters as well as (\" - \", \" ' \", \" . \", \" _ \", for nick names quotation marks (\") are also allowed)")
        )
    
    return value

def validate_character_first_name(value):
    if " " in value:
        raise ValidationError(
            _("First names cannot include spaces. Additional names should be added into the last name box. Characters that are allowed are (-, ', .)")
        )

    if valid_ascii_character(value, False) == False:
        raise ValidationError(
            _("Names can only include alphanumerical characters as well as (\" - \", \" ' \", \" . \", \" _ \", for nick names quotation marks (\") are also allowed)")
        )
    return value

def validate_character_image(value):
    if value.endswith('.png') or value.endswith('.jpg') or value.endswith('.jpeg') or value.endswith('.webp'):
        if "https://" not in value:
            raise ValidationError(
                _("Please submit the full URL (including the https://)")
            )
        return value
    else:
        raise ValidationError(
            _("The URL of your image should be one of these file extensions. (.jpg, .jpeg, .png, .web)"),      
        )
    

def validate_streamer_url(value):
    
    if "twitch" in value or "youtube"  in value or "facebook" in value:
        if "https://" not in value:
            raise ValidationError(
                _("Please submit the full URL (including the https://)")
            )
        return value
    else:
        raise ValidationError(
            _("URL provided is not whitelisted. Whitelisted URLs include facebook, youtube or twitch"), 
            
        )


#make sure a submitted appearance is in the past and not the future
def validate_appearance_time(value):
    #now = pytz.UTC.localize(datetime.now())
    now = timezone.now()
    if value > now:
        raise ValidationError(
            _("Appearance cannot be in the future")
        )   
    else:
        return value
#validate that the clip submitted is a whitelisted URL and that it includes an https protocol
def validate_clip_url(value):
    
    if "twitch" in value or "youtube" in value or "streamable" in value or "facebook" in value:
        if "https://" not in value:
            raise ValidationError(
                _("Please submit the full URL (including the https://)")
            )
        return value
    else:
        raise ValidationError(
            _("Clip provided is not a whitelisted URL. Whitelisted URLS included facebook, youtube, twitch or streamable"), 
            code='invalid'
        )
