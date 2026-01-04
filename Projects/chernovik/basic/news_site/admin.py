from django.contrib import admin
from .models import Category, Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'created_at', 'views')
    list_filter = ('category', 'author', 'created_at')
    search_fields = ('title', 'content')
    fields = ('category', 'title', 'slug', 'image', 'video_file', 'content', 'is_featured', 'is_video')
    prepopulated_fields = {'slug': ('title',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Agar foydalanuvchi SuperAdmin (Siz) bo'lsa, hammani postini ko'radi
        if request.user.is_superuser:
            return qs
        # Agar jurnalist bo'lsa, faqat o'zini postlarini ko'radi
        return qs.filter(author=request.user)

    def save_model(self, request, obj, form, change):
        # Maqola saqlanayotganda muallifni avtomatik joriy foydalanuvchiga biriktirish
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Category)