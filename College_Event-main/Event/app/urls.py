from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm,ChangePasswordForm,MypasswordResetForm,MySetPasswordForm,OrganizerLoginForm,OrganizerChangePasswordForm, OrganizerPasswordResetForm, OrganizerSetPasswordForm
from django.urls import reverse_lazy
from .views import OrganizerLoginView,UserLoginView

app_name = "app"

urlpatterns = [
    
    path("",views.index.as_view(),name='home'),



    path("event/list",views.EventListView.as_view(),name='Eventlist'),
    path('past-events/', views.PastEventListView.as_view(), name='past_event_list'),
    path("event/create",views.EventCreateView.as_view(),name="CreateEvent"),
    path('event/<int:event_id>/register/', views.EventRegistrationView.as_view(), name='event_register'),
     path('registeredEvents/', views.RegisteredEventListView.as_view(), name='registered_Event_list'),
     path('submit_feedback/<int:event_id>/', views.submit_feedback, name='submit_feedback'),
    
#   path('event/<int:event_id>/', views.EventDetailView.as_view(), name='event_detail'),

    #path('event/<int:pk>/update',views.EventUpdateView.as_view(),name='UpdateEvent'),

    path('profile/', views.profile, name='profile'),


    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html',
    authentication_form=LoginForm), name='login'),

    path('logout/', auth_views.LogoutView.as_view(next_page='app:login'), name='logout'),
    

    path('password/change/', auth_views.PasswordChangeView.as_view(template_name='changepassword.html',
    form_class=ChangePasswordForm,success_url="/password/change/done/"),name='password_change'),

    path("password/change/done/",auth_views.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'),
         name='passwordchangedone'),

    path("password/reset/",auth_views.PasswordResetView.as_view(template_name='passwordreset.html'
       ,form_class=MypasswordResetForm),name='passwordreset'),

    path("password-reset/done",auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),

    path("password-reset-confirm/<uidb64>/<token>",auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',
        form_class=MySetPasswordForm),
         name='password_reset_confirm'),
         
    path('password-reset-complete',auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html")
         ,name='password_reset_complete'),

    path('registration/', views.UserRegistrationView.as_view(), name='userRegistration'),


    # Organizer Authentication URLs
     # path('organizer/profile/', views.OrganizerProfileView.as_view(), name='organizerProfile'),

     path('organizer/register/', views.OrganizerRegistrationView.as_view(), name='organizer_registration'),

     path('organizer/login/', auth_views.LoginView.as_view(
        template_name='organizer_login.html',
        authentication_form=OrganizerLoginForm,
        success_url="/event/create"  
    ), name='organizer_login'),

    path('organizer/logout/', views.organizer_logout, name='organizer_logout'),
    path('organizer/password/change/', auth_views.PasswordChangeView.as_view(template_name='organizer_change_password.html', form_class=OrganizerChangePasswordForm, success_url="/organizer/password/change/done/"), name='organizer_password_change'),
    path('organizer/password/change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='organizer_password_changed_done.html'), name='organizer_password_change_done'),
    path('organizer/password/reset/', auth_views.PasswordResetView.as_view(template_name='organizer_password_reset.html', form_class=OrganizerPasswordResetForm), name='organizer_password_reset'),
    path('organizer/password/reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='organizer_password_reset_done.html'), name='organizer_password_reset_done'),
    path('organizer/password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='organizer_password_reset_confirm.html', form_class=OrganizerSetPasswordForm), name='organizer_password_reset_confirm'),
    path('organizer/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='organizer_password_reset_complete.html'), name='organizer_password_reset_complete'),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


