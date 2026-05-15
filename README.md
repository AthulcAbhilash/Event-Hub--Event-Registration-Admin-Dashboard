# Event Hub — Event Registration & Admin Dashboard

A web-based event registration platform with a public event portal, participant registration flow, and an admin dashboard to manage events and registrations.

## Features
### Public Event Portal
- Displays upcoming events in a card-based layout
- Event cards can be opened to view:
  - Event name
  - Description
  - Date
  - Registration option
- Clean and responsive interface for browsing events

### Event Registration
- Registration form opens directly from the selected event
- Collects participant details:
  - Full name
  - Email address
  - Phone number
- Associates each registration with the selected event

### Admin Access
- Separate admin login page
- Protected access to the admin dashboard

### Admin Dashboard
- Shows registration count summary
- Displays event-wise registration statistics
- Allows admins to:
  - Add events
  - Edit existing events
  - Delete events
- Export registration data to Excel

### Registration Management
- View all participant registrations in a table
- Search registrations by:
  - Name
  - Email
  - Phone number
  - Event
- Delete individual registration records

## Tech Stack
- HTML  
- CSS  
- JavaScript  
- Python  
- Flask  

## How to Run
1. Open terminal in the project folder
2. Install Flask if needed:

```bash
pip install flask
```

3. Run the application:

```bash
python app.py
```

4. Open in browser:

```text
http://127.0.0.1:5000
```

## Screenshots
### Event Hub Home
![Event Hub Home](screenshots/event-hub-home)

### Event Card Details
![Event Card Details](screenshots/event-card-details)

### Event Registration Modal
![Event Registration Modal](screenshots/event-registration-modal)

### Admin Login Page
![Admin Login Page](screenshots/admin-login-page)

### Admin Dashboard
![Admin Dashboard](screenshots/admin-dashboard-events)

### Registration Management
![Registration Management](screenshots/registration-management-table)

## Note
- Please do not reuse the personal logo or branding assets without permission.
