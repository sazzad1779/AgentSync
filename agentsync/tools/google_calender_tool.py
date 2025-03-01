import os
import datetime
from typing import Dict, List, Any, Optional

import google.auth
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GoogleCalendarTool:
    def __init__(self, client_secret_file=None):
        """
        Initialize the Google Calendar Tool with authentication
        
        Args:
            client_secret_file: Path to the OAuth client secret file
        """
        # Use config from settings if not provided
        if client_secret_file is None:
            import src.config as settings
            client_secret_file = settings.CLIENT_SECRET_FILE
            
        SCOPES = ["https://www.googleapis.com/auth/calendar"]
        creds = None

        # Check if token file exists
        if os.path.exists(client_secret_file):
            try:
                creds = Credentials.from_authorized_user_file(client_secret_file, SCOPES)
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(google.auth.transport.requests.Request())  # Refresh expired token
            except Exception as e:
                print(f"⚠️ Error loading credentials: {e}")
                creds = None  # Force re-authentication

        # If credentials are not available, authenticate
        if not creds or not creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
            creds = flow.run_local_server(port=0)
            # Save new token
            with open(client_secret_file, "w") as token:
                token.write(creds.to_json())
                
        self.service = build("calendar", "v3", credentials=creds)
        print("✅ Google Calendar API authenticated")

    def create_event(self, summary, start_time, end_time, description="", location="", attendees=None):
        """
        Create a new calendar event
        
        Args:
            summary: Title of the event
            start_time: Start time in ISO format (YYYY-MM-DDTHH:MM:SS)
            end_time: End time in ISO format (YYYY-MM-DDTHH:MM:SS)
            description: Description of the event
            location: Location of the event
            attendees: List of email addresses to invite
            
        Returns:
            Dict with event details or error message
        """
        try:
            event_body = {
                'summary': summary,
                'description': description,
                'start': {'dateTime': start_time, 'timeZone': 'UTC'},
                'end': {'dateTime': end_time, 'timeZone': 'UTC'},
            }
            
            if location:
                event_body['location'] = location
                
            if attendees:
                event_body['attendees'] = [{'email': email} for email in attendees]
            
            # Create the event
            event = self.service.events().insert(calendarId='primary', body=event_body).execute()
            
            print(f"✅ Event created: {summary}")
            return {
                "success": True,
                "event_id": event.get('id'),
                "link": event.get('htmlLink')
            }
            
        except HttpError as e:
            print(f"❌ Error creating event: {e}")
            return {"success": False, "error": str(e)}

    def list_events(self, max_results=10):
        """
        List upcoming calendar events
        
        Args:
            max_results: Maximum number of events to return
            
        Returns:
            Dict containing list of events or error message
        """
        try:
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            if not events:
                print("ℹ️ No upcoming events found")
                return {"success": True, "events": []}
            
            # Format events
            formatted_events = []
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))
                
                formatted_events.append({
                    'id': event['id'],
                    'summary': event.get('summary', 'Untitled Event'),
                    'start': start,
                    'end': end,
                    'description': event.get('description', ''),
                    'location': event.get('location', '')
                })
            
            print(f"✅ Retrieved {len(formatted_events)} events")
            return {"success": True, "events": formatted_events}
            
        except HttpError as e:
            print(f"❌ Error listing events: {e}")
            return {"success": False, "error": str(e)}

    def delete_event(self, event_id):
        """
        Delete a calendar event
        
        Args:
            event_id: ID of the event to delete
            
        Returns:
            Dict with success status or error message
        """
        try:
            self.service.events().delete(calendarId='primary', eventId=event_id).execute()
            print(f"✅ Event {event_id} deleted")
            return {"success": True}
        except HttpError as e:
            print(f"❌ Error deleting event: {e}")
            return {"success": False, "error": str(e)}

    def update_event(self, event_id, summary=None, start_time=None, end_time=None, 
                    description=None, location=None):
        """
        Update an existing calendar event
        
        Args:
            event_id: ID of the event to update
            summary: New title of the event
            start_time: New start time in ISO format
            end_time: New end time in ISO format
            description: New description of the event
            location: New location of the event
            
        Returns:
            Dict with updated event details or error message
        """
        try:
            # Get the existing event
            event = self.service.events().get(calendarId='primary', eventId=event_id).execute()
            
            # Update fields that are provided
            if summary:
                event['summary'] = summary
            if description:
                event['description'] = description
            if location:
                event['location'] = location
            if start_time:
                event['start']['dateTime'] = start_time
            if end_time:
                event['end']['dateTime'] = end_time
            
            # Update the event
            updated_event = self.service.events().update(
                calendarId='primary', eventId=event_id, body=event
            ).execute()
            
            print(f"✅ Event updated: {updated_event.get('summary')}")
            return {
                "success": True, 
                "event_id": updated_event.get('id'),
                "link": updated_event.get('htmlLink')
            }
            
        except HttpError as e:
            print(f"❌ Error updating event: {e}")
            return {"success": False, "error": str(e)}


# For LangGraph integration
def get_calendar_tools():
    """Return calendar tools formatted for LangGraph"""
    calendar = GoogleCalendarTool()
    
    return {
        "schedule_event": {
            "description": "Schedule a new event in Google Calendar",
            "function": lambda kwargs: calendar.create_event(**kwargs),
            "parameters": {
                "type": "object",
                "properties": {
                    "summary": {"type": "string", "description": "Event title"},
                    "start_time": {"type": "string", "description": "Start time (YYYY-MM-DDTHH:MM:SS)"},
                    "end_time": {"type": "string", "description": "End time (YYYY-MM-DDTHH:MM:SS)"},
                    "description": {"type": "string", "description": "Event description"},
                    "location": {"type": "string", "description": "Event location"},
                    "attendees": {"type": "array", "items": {"type": "string"}, "description": "List of email addresses"}
                },
                "required": ["summary", "start_time", "end_time"]
            }
        },
        "get_events": {
            "description": "List upcoming events in your Google Calendar",
            "function": lambda kwargs: calendar.list_events(**kwargs),
            "parameters": {
                "type": "object",
                "properties": {
                    "max_results": {"type": "integer", "description": "Maximum number of events to return"}
                }
            }
        },
        "cancel_event": {
            "description": "Cancel (delete) an event from your calendar",
            "function": lambda kwargs: calendar.delete_event(**kwargs),
            "parameters": {
                "type": "object",
                "properties": {
                    "event_id": {"type": "string", "description": "ID of the event to delete"}
                },
                "required": ["event_id"]
            }
        },
        "modify_event": {
            "description": "Modify an existing calendar event",
            "function": lambda kwargs: calendar.update_event(**kwargs),
            "parameters": {
                "type": "object",
                "properties": {
                    "event_id": {"type": "string", "description": "ID of the event to update"},
                    "summary": {"type": "string", "description": "New event title"},
                    "start_time": {"type": "string", "description": "New start time"},
                    "end_time": {"type": "string", "description": "New end time"},
                    "description": {"type": "string", "description": "New description"},
                    "location": {"type": "string", "description": "New location"}
                },
                "required": ["event_id"]
            }
        }
    }


# Example usage
if __name__ == "__main__":
    # Simple test
    calendar = GoogleCalendarTool()
    
    # List events
    events = calendar.list_events(max_results=5)
    print(events)
    
    # # Create event (tomorrow at noon for 1 hour)
    # tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
    # tomorrow_noon = tomorrow.replace(hour=12, minute=0, second=0).isoformat()
    # tomorrow_1pm = tomorrow.replace(hour=13, minute=0, second=0).isoformat()
    
    # result = calendar.create_event(
    #     summary="Test Event",
    #     start_time=tomorrow_noon,
    #     end_time=tomorrow_1pm,
    #     description="This is a test event created by the GoogleCalendarTool"
    # )
    # print(result)