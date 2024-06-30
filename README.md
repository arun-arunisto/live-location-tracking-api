# Live Location Tracking API

This project is a live location tracking system similar to those used by Swiggy and Zomato. It is built using Django and Django REST Framework for the backend, and OpenStreetMap API for the frontend map. The system utilizes JavaScript for collecting latitude and longitude data, and employs Channels and WebSockets to transfer this data from the frontend to the backend.

## Features

- **User Management**: Admin users can create and manage users.
- **Destination Setting**: Admin can set destinations for users.
- **Live Tracking**: Tracks the user's location from the starting point to the destination.
- **Error Handling**: Continuously checks for network errors every 3 seconds and attempts to clear them.
- **Status Indicators**: Shows 'Stopped' when the user stops and 'Travelling' when the user moves.
- **Conditional Data Updates**: Live location data updates only when the user is moving.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/arun-arunisto/live-location-tracking-api.git
   cd tracking-project
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Start the Django development server:**
   ```bash
   python manage.py runserver
   ```

5. **Set up Channels:**
   - Configure Channels layers in `settings.py`.



## Usage

1. **Admin User:**
   - Log in as an admin.
   - Create users and set destinations for them.

2. **User:**
   - Accept the destination request.
   - The system will track your location from the starting point to the destination.
   - If you stop moving, the system will show 'Stopped' and pause location updates.
   - When you resume moving, the system will show 'Travelling' and resume location updates.

## Technologies Used

- Django
- Django REST Framework
- OpenStreetMap API
- JavaScript
- Channels
- WebSockets

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss what you would like to change.
