from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from djangoapp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("djangoapp/", include("djangoapp.urls")),
    path("about", TemplateView.as_view(template_name="About.html"), name="about"),
    path("contact", TemplateView.as_view(template_name="Contact.html"), name="contact"),
    path("login", views.login_page, name="login_page"),
    path("register", views.register_page, name="register_page"),
    path("dealers", views.home_page, name="dealers_page"),
    path("dealers/state/<str:state>", views.dealers_state_page, name="dealers_by_state_page"),
    path("dealer/<int:dealer_id>", views.dealer_page, name="dealer_page"),
    path("postreview/<int:dealer_id>", views.post_review_page, name="post_review_page"),
    path("", views.home_page, name="home"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
