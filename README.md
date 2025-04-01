# Nexus - Process Manager

Nexus is a powerful web-based application built with Python and Django that enables comprehensive monitoring and management of server processes. Utilizing a lightweight frontend architecture with HTMX and Django templates, the application provides a responsive and efficient user experience without the overhead of a traditional JavaScript framework.
Key Features:

- Real-time monitoring of active server processes
- Process termination capability for quick resource management
- Process snapshot functionality to capture system state at specific moments
- Export capabilities to Excel files for offline analysis and reporting
- Intuitive user interface with minimal page refreshes thanks to HTMX

This monitoring solution gives system administrators and DevOps professionals the tools they need to maintain server health and optimize performance. By combining Django's robust backend with HTMX's efficient frontend approach, Nexus delivers powerful functionality with minimal resource consumption.

## TODO
- [ ] Reorganize templates structure (e.g., use Django's template inheritance)
- [ ] Improve UI
- [ ] Change tailwind from CDN to local
- [ ] Add more tests
- [ ] Consider using "real" database instead of SQLite


## Configuration

To properly configure and run Nexus, you need to set up a security key. This can be done in one of two ways:

### Using Environment Variables
Export the `SECRET_KEY` environment variable on your server:

```bash
export SECRET_KEY="your_long_and_secure_key_here"
```

For permanent configuration, add this line to your shell profile file (e.g., `.bashrc`, `.zshrc`, or `/etc/environment`).

### Using a .env File
Alternatively, create a `.env` file in the root directory of the application and specify the SECRET_KEY:

```
SECRET_KEY=your_long_and_secure_key_here
```

### Security Recommendations
- Generate a strong, random key with sufficient length (at least 50 characters)
- Never commit your `.env` file or hard-coded keys to version control
- Rotate your keys periodically to maintain security
- Restrict access permissions to both the environment variable and `.env` file

The application will automatically detect and use the SECRET_KEY whether it's set as an environment variable or in the `.env` file.


## Nexus Startup Guide

This guide will help you get Nexus up and running quickly.

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps

#### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/nexus.git
cd nexus
```

#### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure Environment
Set up your SECRET_KEY as described in the configuration section.

#### 5. Run Database Migrations
```bash
python manage.py migrate
```

#### 6. Create Admin User
```bash
python manage.py createsuperuser
```

#### 7. Start the Server

#### Development Server
```bash
python manage.py runserver
```

#### Production Deployment with Gunicorn

1. Install Gunicorn:
```bash
pip install gunicorn
```

2. Run with Gunicorn:
```bash
gunicorn nexus.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

3. For background processing, use:
```bash
gunicorn nexus.wsgi:application --bind 0.0.0.0:8000 --workers 3 --daemon
```

### Nginx Configuration for Production

For production environments, it's recommended to use Nginx as a reverse proxy:

1. Install Nginx:
```bash
# Ubuntu/Debian
sudo apt install nginx

# CentOS/RHEL
sudo yum install nginx
```

2. Create an Nginx configuration file:
```
server {
    listen 80;
    server_name your-domain.com;

    location /static/ {
        alias /path/to/nexus/static/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

3. Test and restart Nginx:
```bash
sudo nginx -t
sudo systemctl restart nginx
```

### Systemd Service (For Automatic Startup)

Create a systemd service file to automatically start Nexus on system boot:

```bash
sudo nano /etc/systemd/system/nexus.service
```

Add the following content:
```
[Unit]
Description=Nexus Server Process Monitor
After=network.target

[Service]
User=your_user
Group=your_group
WorkingDirectory=/path/to/nexus
ExecStart=/path/to/nexus/venv/bin/gunicorn nexus.wsgi:application --bind 127.0.0.1:8000 --workers 3
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl enable nexus
sudo systemctl start nexus
```

### Access the Application
Once running, access Nexus at: http://127.0.0.1:8000/ or http://your-domain.com/

## License
Custom license, see LICENSE.md for more details.
