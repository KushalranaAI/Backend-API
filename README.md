# Google Calendar Integration with Django REST API and OAuth 2.0

This project demonstrates how to integrate Google Calendar using Django REST API with OAuth2 authentication.

## Getting Started

These instructions will help you set up the project on your local machine for development and testing purposes.

### Prerequisites

- Python 3.6 (minimun)
- Django
- Django REST Framework
- Google API Client Library

### Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/KushalranaAI/google-calendar-integration.git
   
2. Navigate to the project directory:

    ```shell
    cd google-calendar-integration


3. Install the required Python packages:

    ```shell
    pip install -r requirements.txt

4. Set up Google OAuth Credentials:

- Go to the Google Cloud Console (https://console.cloud.google.com/).
- Create a new project or select an existing project.
- Enable the "Google Calendar API" for your project.
- Create OAuth 2.0 credentials and download the JSON file.
- Rename the downloaded JSON file to credentials.json and place it in the project's root directory.

5. Apply database migrations:

      ```shell
      python manage.py migrate

6. Start the development server:

    ```shell
    python manage.py runserver

7. Access the API endpoints:

- Initiate OAuth2 flow:

      ```bash
      GET http://localhost:8000/rest/v1/calendar/init/
- Handle OAuth2 redirect:

      ```ruby
      GET http://localhost:8000/rest/v1/calendar/redirect/?code=<authorization_code>&state=<state_value>

- Retrieve events from the calendar:

      ```bash
      GET http://localhost:8000/rest/v1/calendar/events/
        
##License
This project is licensed under the MIT License - see the LICENSE file for details.

Feel free to modify and format the content as per your requirements.
