from django.contrib import admin

# Register your models here.
class UnindexedAdmin(admin.ModelAdmin):

    def get_model_perms(self, request):
        """
        Hide the the model from admin index by returning an empty perms dict.
        """
        return {}
