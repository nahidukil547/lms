from django.contrib import admin
from .models import UserProfile,Course,Module,Lesson,RecodedVideo,Enrollment,Assignment, Submission

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(RecodedVideo)
admin.site.register(Enrollment)
admin.site.register(Assignment)
admin.site.register(Submission)