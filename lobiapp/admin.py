from django.contrib import admin
from.models import ChatBookmark, ChatMessage, ChatReply, Evaluation, Group, GroupMember, MyUser
# Register your models here.
admin.site.register(MyUser)
admin.site.register(Group)
admin.site.register(GroupMember)
admin.site.register(ChatMessage)
admin.site.register(ChatReply)
admin.site.register(ChatBookmark)
admin.site.register(Evaluation)