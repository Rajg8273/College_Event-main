from django.views.generic import TemplateView
from app.forms import UserRegistrationForm, OrganizerRegistrationForm
from django.shortcuts import render,redirect    
from django.contrib import messages
from django.views import View
from .forms import EventForm,FeedbackForm
from .models import Event
from datetime import datetime, timedelta
from django.contrib.auth import logout as django_logout
from django.views.generic import ListView
from .models import Event, Feedback, Participant,Organizer
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.views import LoginView
from .forms import OrganizerLoginForm,LoginForm

from django.shortcuts import get_object_or_404
from django.db.models import Exists, OuterRef

from joblib import load

model = load('../SaveModel/model.joblib')

class FeedbackPredictor(View):
    # def __init__(self):
    #     # Load the pre-trained model
    #     self.model = joblib.load('your_model_path.pkl')  # Replace 'your_model_path.pkl' with the actual path to your model file
        
    def post(self, request):
        if request.method == "POST":
            # Extract features from the request
            organizer_name = request.POST['organizer_name']
            event_year = int(request.POST['event_year'])  # Convert to int if needed
            event_month = int(request.POST['event_month'])  # Convert to int if needed
            event_day = int(request.POST['event_day'])  # Convert to int if needed
            
            # Prepare input data
            X = [[organizer_name, event_year, event_month, event_day]]
            
            # Make prediction
            y_pred = self.model.predict(X)
            
            # Map prediction to feedback score categories
            if y_pred == 0:
                feedback_score = "Low"
            elif y_pred == 1:
                feedback_score = "Medium"
            else:
                feedback_score = "High"
            
            return render(request, 'main.html', {'result': feedback_score})
        
        return render(request, 'main.html')

class EventRegistrationView(View):
    def post(self, request, event_id):
        # Retrieve the event object based on the event_id
        event = get_object_or_404(Event, id=event_id)
        
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Create or get the participant object for the current user and event
            participant, created = Participant.objects.get_or_create(user=request.user, event=event)
            
            # Check if the participant was created or already exists
            if created:
                messages.success(request, "Registered successfully!")
            else:
                messages.info(request, "You are already registered for this event.")
            
            # Redirect the user to the registered event page
            return redirect('app:Eventlist')
        else:
            # If user is not authenticated, display an error message
            messages.error(request, "Please login to register for the event.")
            # Redirect the user to the login page
            return redirect('app:login')  
        

def submit_feedback(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    # Check if the user has already given feedback for this event
    participant = Participant.objects.filter(user=request.user, event=event).first()
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            comment = form.cleaned_data['comment']
            if participant and participant.feedbacks.exists():
                # If feedback already exists, update it
                feedback = participant.feedbacks.first()
                feedback.rating = rating
                feedback.comment = comment
                feedback.save()
                messages.success(request, "Your feedback has been updated successfully!")
            else:
                # If no feedback exists, create a new one
                Feedback.objects.create(event=event, participant=participant, rating=rating, comment=comment)
                messages.success(request, "Thank you for your feedback!")
            # return redirect('app:registered_Event_list')  # Redirect to event detail page or anywhere you prefer
    else:
        # Prepopulate the form if feedback exists
        initial_data = {}
        if participant and participant.feedbacks.exists():
            feedback = participant.feedbacks.first()
            initial_data['rating'] = feedback.rating
            initial_data['comment'] = feedback.comment
            form = FeedbackForm(initial=initial_data)
        else:
            form = FeedbackForm()
    
    return render(request, 'feedback_form.html', {'form': form, 'event': event})
        
        
class RegisteredEventListView(ListView):
    template_name = 'event_registered_list.html'
    context_object_name = 'registered_events'

    def get_queryset(self):
        # Annotate each event with a boolean indicating whether the user has given feedback
        queryset = Event.objects.filter(participants__user=self.request.user).annotate(
            feedback_given=Exists(Feedback.objects.filter(event=OuterRef('pk'), participant__user=self.request.user))
        )
        return queryset
    





def profile(request):
    return render(request, 'profile.html')

class EventCreateView(View):
    form_class = EventForm
    template_name = 'event_create.html'

    def get(self, request, *args, **kwargs):
        if hasattr(request.user, 'organizer'):
            form = self.form_class()
            return render(request, self.template_name, {'form': form})
        else:
            # Handle the case where the logged-in user doesn't have an organizer profile
            return redirect('app:home') 

    def post(self, request, *args, **kwargs):
        if hasattr(request.user, 'organizer'):
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                event = form.save(commit=False)
                event.organizer = request.user.organizer
                event.save()
                return redirect('app:Eventlist') 
            return render(request, self.template_name, {'form': form})
        else:
           
            return redirect('app:home')  




class UserLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = LoginForm
    success_url = reverse_lazy('app:home')  

def organizer_logout(request):
    # Log out the user
    django_logout(request)
    return redirect('app:home')

class OrganizerLoginView(LoginView):
    template_name = 'organizer_login.html'
    authentication_form = OrganizerLoginForm
    success_url = reverse_lazy('app:CreateEvent') 
 



class UserRegistrationView(View):
  def get(self,request):
        form=UserRegistrationForm()
        return render(request,'userRegistration.html',{'form':form})

  def post(self,request):
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
           messages.success(request,"Congratulation!! Registered Sucessfully")
           form.save()
           return redirect('app:login')
        return render(request,'userRegistration.html',{'form':form})
  

class OrganizerRegistrationView(View):
    def get(self, request):
        form = OrganizerRegistrationForm()
        return render(request, 'organizer_registration.html', {'form': form})

    def post(self, request):
        form = OrganizerRegistrationForm(request.POST)
        if form.is_valid():
            # Save the user
            user = form.save(commit=False)
            user.save()
            
            # If 'is_organizer' checkbox is checked, create an Organizer instance
            if form.cleaned_data['is_organizer']:
                Organizer.objects.create(user=user, organization_name=form.cleaned_data['organization_name'], 
                                         contact_email=form.cleaned_data['contact_email'])
            
            messages.success(request, "Congratulations! Registered successfully.")
            return redirect('app:organizer_login')  # Redirect to organizer login page after successful registration
        return render(request, 'organizer_registration.html', {'form': form})


class OrganizerFeedbackView(View):
    def get(self, request):
        # Assuming you have a one-to-one relationship between User and Organizer models
        organizer = request.user.organizer
        events = Event.objects.filter(organizer=organizer)
        feedbacks = Feedback.objects.filter(event__in=events)
        return render(request, 'organizer_feedback.html', {'feedbacks': feedbacks})


class OrganizerParticipantsView(View):
    def get(self, request):
        # Assuming you have a one-to-one relationship between User and Organizer models
        organizer = request.user.organizer
        events = Event.objects.filter(organizer=organizer)
        participants = Participant.objects.filter(event__in=events)
        return render(request, 'organizer_participants.html', {'participants': participants})


class index(TemplateView):
     def get(self, request):
        # Get today's date
        today = datetime.now().date()

        # Define dictionaries to store events for each day
        events_by_day = {
        }

        # Get events for each day
        for i in range(4):
            # Calculate the day
            day = today + timedelta(days=i)
            # Get events for the day
            events = Event.objects.filter(date=day)
            # Store events in the dictionary
            events_by_day[f'day{i+1}'] = events
        return render(request, 'home.html', {'events_by_day': events_by_day})



class EventListView(View):
    def __init__(self):
        super().__init__()
        # Load your machine learning model
        self.model = load('../SaveModel/model.joblib')
    
    def get(self, request):
        # Get today's date
        today = datetime.now().date()

        # Define dictionaries to store events for each day
        events_by_day = {}

        # Get events for each day
        for i in range(7):
            # Calculate the day
            day = today + timedelta(days=i)
            # Get events for the day
            events = Event.objects.filter(date=day)
            # Store events in the dictionary
            events_by_day[f'day{i+1}'] = events

        # Fetch comments related to events
        for events in events_by_day.values():
            for event in events:
                event.comments = event.feedbacks.all()  

                # Check if the events are already registered by the user
                event.is_registered = event.participants.filter(user=request.user).exists()

        # Render the template with events
        return render(request, 'event_list.html', {'events_by_day': events_by_day})
    
    def post(self, request):
        # Get event ID from POST data
        event_id = request.POST.get('event_id')

        # Fetch event data from database
        event = Event.objects.get(id=event_id)

        # Prepare input data for prediction
        organizer=0
        if event.organizer=="TTA":
            organizer = 5

        input_data = [[organizer, event.date.year, event.date.month, event.date.day]]

        # Make prediction using the loaded model
        feedback_prediction = self.model.predict(input_data)

        # Return JSON response with predicted feedback
        return JsonResponse({'feedback_prediction': feedback_prediction})
    
    
class PastEventListView(View):
    def get(self, request):
        # Get today's date
        today = timezone.now().date()

        # Get past events in descending order of date
        past_events = Event.objects.filter(date__lt=today).order_by('-date')

        # Fetch comments related to past events
        for event in past_events:
            event.comments = event.feedbacks.all()  

            # Check if the events are already registered by the user
            event.is_registered = event.participants.filter(user=request.user).exists()

        # Render the template with past events
        return render(request, 'past_event_list.html', {'past_events': past_events})
    

class OrganizerProfileView(View):
    def get(self, request):
        form = EventForm()
        return render(request, 'organizer_profile.html', {'form': form})

    def post(self, request):
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            # Assuming you have a one-to-one relationship between User and Organizer models
            organizer = request.user.organizer
            event.organizer = organizer
            event.save()
            return redirect('home')  # Redirect to the home page or event detail page
        return render(request, 'organizer_profile.html', {'form': form})
    

# class EventDetailView(View):
#     def get(self, request, event_id):
#         event = Event.objects.get(id=event_id)
#         return render(request, 'event_detail.html', {'event': event})


