from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import TodoItem

## calendar
from googleapiclient import discovery
from oauth2client import tools
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
import httplib2

# Create your views here.
def todoView(request):
    all_todo_items = TodoItem.objects.all()
    return render(request,
    'todo/index.html',
    {'all_items':all_todo_items})
def addTodo(request):
    new_item = TodoItem(item = request.POST['item'])
    new_item.save()
    return HttpResponseRedirect('/todo/')
def deleteTodo(request,todo_id):
    item_to_delete = TodoItem.objects.get(id=todo_id)
    item_to_delete.delete()
    return HttpResponseRedirect('/todo/')


#---------------------------------------------------------------------------
# google_calendar_connection
#---------------------------------------------------------------------------
def google_calendar_connection():
    """
    This method used for connect with google calendar api.
    """
    
    flags = tools.argparser.parse_args([])
    FLOW = OAuth2WebServerFlow(
        client_id='869278056257-datlsbfg8i283sub2sb5g8lkn51eotfi.apps.googleusercontent.com',
        client_secret='EO6Vdgyse017dUpokAIOpTu8',
        scope='https://www.googleapis.com/auth/calendar',
        user_agent='todo-app-1604161650593'
        )
    storage = Storage('calendar.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid == True:
        credentials = tools.run_flow(FLOW, storage, flags)
        
    # Create an httplib2.Http object to handle our HTTP requests and authorize it
    # with our good Credentials.
    http = httplib2.Http()
    http = credentials.authorize(http)
    service = discovery.build('calendar', 'v3', http=http)
        
    return service



def form_valid(self, form):
    """
    This method used for add event in google calendar.
    """
        
    service = self.google_calendar_connection()
        
    event = {
      'summary': "new",
      'location': "london",
      'description': "anything",
      'start': {
        'date': "2015-09-02",
      },
      'end': {
        'date': "2015-09-02",
      },
             
    }
        
    event = service.events().insert(calendarId='primary', body=event).execute()
        
    return CreateView.form_valid(self, form) 
