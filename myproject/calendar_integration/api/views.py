import json
import os
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.urls import reverse
from django.views import View
from google.auth import exceptions
from google.oauth2 import credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from django.shortcuts import redirect
from urllib.parse import urlparse, urlencode, parse_qs


class GoogleCalendarInitView(View):
    def get(self, request):
        flow = Flow.from_client_secrets_file(
            os.path.join(settings.BASE_DIR, 'credentials.json'),
            scopes=['https://www.googleapis.com/auth/calendar.readonly'],
            redirect_uri=request.build_absolute_uri(
                reverse('google_calendar_redirect'))
        )
        authorization_url, state = flow.authorization_url(prompt='consent')

        # Parse the authorization URL to extract the query parameters
        parsed_url = urlparse(authorization_url)
        query_params = parse_qs(parsed_url.query)

        # Add the 'access_type' parameter with the value 'offline'
        query_params['access_type'] = 'offline'

        # Reconstruct the authorization URL with the updated query parameters
        updated_url = parsed_url._replace(
            query=urlencode(query_params, doseq=True)).geturl()

        # Redirect the user to the updated authorization URL
        return redirect(updated_url)



class GoogleCalendarRedirectView(View):
    def get(self, request):
        code = request.GET.get('code')
        state = request.GET.get('state')

        if not code:
            return HttpResponseBadRequest('Authorization code is missing')

        flow = Flow.from_client_secrets_file(
            os.path.join(settings.BASE_DIR, 'credentials.json'),
            scopes=['https://www.googleapis.com/auth/calendar.readonly'],
            redirect_uri=request.build_absolute_uri(
                reverse('google_calendar_redirect')),
            state=state
        )

        try:
            flow.fetch_token(code=code)
            credentials_data = flow.credentials.to_json()
        except exceptions.GoogleAuthError as e:
            return HttpResponseBadRequest(f'Failed to fetch token: {str(e)}')

        credentials_obj = credentials.Credentials.from_authorized_user_info(
            json.loads(credentials_data))  # Convert JSON string to dictionary
        service = build('calendar', 'v3', credentials=credentials_obj)
        events = service.events().list(calendarId='primary').execute()
        event_list = events.get('items', [])

        return JsonResponse({'events': event_list})
