import socket
import network
import time
import gc
from machine import Pin
import urequests

led = Pin(2, Pin.OUT)  # On-board LED for status indication

WIFI_SSID = "YOUR_WIFI_NAME"  # TODO: Replace with your WiFi SSID
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"  # TODO: Replace with your WiFi password

GITHUB_USERNAME = "utk09-NCL"  # TODO: Replace with your GitHub username
GITHUB_REPO = "esp32-ghw-26"  # TODO: Replace with your repository name
GITHUB_FILEPATH = (
    "portfolios.json"  # TODO: Replace with the path to your JSON file in the repo
)

GITHUB_URL = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{GITHUB_REPO}/main/{GITHUB_FILEPATH}"

portfolio_cache = None
last_fetch_time = 0
CACHE_DURATION = 300  # Cache duration in seconds (5 minutes)


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if wlan.isconnected():
        ip = wlan.ifconfig()[0]
        print(f" Connected to WiFi. IP: {ip}")
        return ip

    print(f" Connecting to WiFi {WIFI_SSID}...")
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    for _ in range(10):
        if wlan.isconnected():
            ip = wlan.ifconfig()[0]
            print(f" Connected to WiFi. IP: {ip}")
            return ip
        time.sleep(1)
        print(" Attempting to connect...")

    print(" Failed to connect to WiFi.")
    return None


def fetch_portfolios_data():
    global portfolio_cache, last_fetch_time
    current_time = time.time()
    if portfolio_cache and (current_time - last_fetch_time < CACHE_DURATION):
        print(" Using cached portfolio data.")
        return portfolio_cache

    print(" Fetching portfolio data from GitHub...")
    print(f" URL: {GITHUB_URL}")

    try:
        response = urequests.get(GITHUB_URL)
        if response.status_code == 200:
            portfolios_data = response.json()
            response.close()

            if isinstance(portfolios_data, list):
                portfolio_cache = portfolios_data
                last_fetch_time = current_time
                print(" Portfolio data fetched successfully.")
                return portfolios_data
        else:
            print(f" Failed to fetch data. Status code: {response.status_code}")
            response.close()
            return []
    except Exception as e:
        print(f" Exception occurred while fetching data: {e}")
        return []


def generate_home_page(portfolios):
    user_cards = ""
    for portfolio in portfolios:
        github_username = portfolio.get("github", "").lower()
        full_name = portfolio.get("fullName", "Unknown")
        title = portfolio.get("title", "N/A")

        user_cards += f"""<div class="user-card">
            <div class="user-pic">{full_name[0]}</div>
            <h3>{full_name}</h3>
            <p>{title}</p>
            <a href="/{github_username}" class="view-btn">View Portfolio →</a>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ESP-32 Portfolio Web Server</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}

        .container {{
            max-width: 1000px;
            margin: 0 auto;
        }}

        header {{
            text-align: center;
            color: white;
            margin-bottom: 50px;
        }}

        h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        .subtitle {{
            font-size: 1.1em;
            opacity: 0.9;
        }}

        .users-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}

        .user-card {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.3s, box-shadow 0.3s;
        }}

        .user-card:hover {{
            transform: translateY(-10px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }}

        .user-pic {{
            width: 100px;
            height: 100px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea, #764ba2);
            margin: 0 auto 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 40px;
            color: white;
        }}

        .user-card h3 {{
            color: #333;
            margin-bottom: 8px;
            font-size: 1.3em;
        }}

        .user-card p {{
            color: #666;
            margin-bottom: 20px;
            font-size: 0.95em;
        }}

        .view-btn {{
            display: inline-block;
            padding: 10px 20px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            text-decoration: none;
            border-radius: 25px;
            transition: transform 0.3s;
            font-weight: 600;
        }}

        .view-btn:hover {{
            transform: scale(1.05);
        }}

        .footer {{
            text-align: center;
            color: white;
            padding: 20px;
            font-size: 0.9em;
        }}

        .esp32-badge {{
            background: rgba(255,255,255,0.2);
            color: white;
            padding: 5px 15px;
            border-radius: 15px;
            display: inline-block;
            margin-top: 10px;
        }}

        @media (max-width: 600px) {{
            h1 {{ font-size: 1.8em; }}
            .users-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🌟 Portfolios</h1>
            <p class="subtitle">Click on any user card to view their portfolio</p>
        </header>

        <div class="users-grid">
            {user_cards}
        </div>

        <div class="footer">
            <div>Powered by ESP32 + MicroPython</div>
            <div class="esp32-badge">🚀 Running on IoT Hardware</div>
        </div>
    </div>
</body>
</html>"""

    return html


def generate_portfolio_html(portfolio_data):
    full_name = portfolio_data.get("fullName", "Portfolio")
    title = portfolio_data.get("title", "Developer")
    github = portfolio_data.get("github", "")
    linkedin = portfolio_data.get("linkedin", "")
    email = portfolio_data.get("email", "")
    about = portfolio_data.get("about", "Welcome to my portfolio")
    skills = portfolio_data.get("skills", [])
    projects = portfolio_data.get("projects", [])

    skills_html = "".join([f'<span class="skill">{skill}</span>' for skill in skills])

    projects_html = ""
    for project in projects:
        project_url = project.get("url", "")
        url_link = (
            f'<a href="{project_url}" target="_blank">View Project →</a>'
            if project_url
            else ""
        )
        projects_html += f"""<div class="project">
            <h3>{project.get("name", "Project")}</h3>
            <p>{project.get("description", "")}</p>
            {url_link}
        </div>"""

    social_links = ""
    if github:
        social_links += (
            f'<a href="https://github.com/{github}" target="_blank">GitHub</a>'
        )
    if linkedin:
        social_links += (
            f'<a href="https://linkedin.com/in/{linkedin}" target="_blank">LinkedIn</a>'
        )
    if email:
        social_links += f'<a href="mailto:{email}">Email</a>'

    back_link = '<a href="/" class="back-link">← Back to All Portfolios</a>'

    skills_section = ""
    if skills:
        skills_section = f"""<div class="section">
            <h2>Skills</h2>
            <div class="skills">{skills_html}</div>
        </div>"""

    projects_section = ""
    if projects:
        projects_section = f"""<div class="section">
            <h2>Projects</h2>
            {projects_html}
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{full_name} - Portfolio</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}

        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}

        .back-link {{
            display: inline-block;
            color: white;
            text-decoration: none;
            margin-bottom: 20px;
            font-weight: 600;
            transition: transform 0.3s;
        }}

        .back-link:hover {{
            transform: translateX(-5px);
        }}

        header {{
            background: white;
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}

        .profile-pic {{
            width: 120px;
            height: 120px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea, #764ba2);
            margin: 0 auto 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 48px;
            color: white;
        }}

        h1 {{
            color: #333;
            margin-bottom: 10px;
            font-size: 2.5em;
        }}

        .title {{
            color: #666;
            font-size: 1.2em;
            margin-bottom: 20px;
        }}

        .social-links {{
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }}

        .social-links a {{
            padding: 10px 20px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 25px;
            transition: transform 0.3s;
        }}

        .social-links a:hover {{
            transform: translateY(-2px);
        }}

        .section {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}

        h2 {{
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.8em;
        }}

        .about {{
            font-size: 1.1em;
            color: #555;
            line-height: 1.8;
        }}

        .skills {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 15px;
        }}

        .skill {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9em;
        }}

        .project {{
            border-left: 4px solid #667eea;
            padding-left: 20px;
            margin-bottom: 20px;
        }}

        .project h3 {{
            color: #333;
            margin-bottom: 8px;
        }}

        .project p {{
            color: #666;
            margin-bottom: 10px;
        }}

        .project a {{
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
        }}

        .project a:hover {{
            text-decoration: underline;
        }}

        .footer {{
            text-align: center;
            color: white;
            padding: 20px;
            font-size: 0.9em;
        }}

        .esp32-badge {{
            background: rgba(255,255,255,0.2);
            color: white;
            padding: 5px 15px;
            border-radius: 15px;
            display: inline-block;
            margin-top: 10px;
        }}

        @media (max-width: 600px) {{
            h1 {{ font-size: 1.8em; }}
            .social-links {{ flex-direction: column; }}
            .container {{ padding: 10px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        {back_link}

        <header>
            <div class="profile-pic">{full_name[0]}</div>
            <h1>{full_name}</h1>
            <div class="title">{title}</div>
            <div class="social-links">
                {social_links}
            </div>
        </header>

        <div class="section">
            <h2>About Me</h2>
            <div class="about">{about}</div>
        </div>

        {skills_section}

        {projects_section}

        <div class="footer">
            <div>Powered by ESP32 + MicroPython</div>
            <div class="esp32-badge">🚀 Running on IoT Hardware</div>
        </div>
    </div>
</body>
</html>"""

    return html


def parse_request_path(request):
    try:
        lines = request.split("\r\n")
        if lines:
            parts = lines[0].split(" ")
            if len(parts) >= 2:
                path = parts[1].lower()
                return path
    except Exception as e:
        print(f" Error parsing request path: {e}")
    return "/"


def find_portfolio(portfolios, github_username):
    for portfolio in portfolios:
        if portfolio.get("github", "").lower() == github_username.lower():
            return portfolio
    return None


def start_portfolio_server():
    ip = connect_wifi()
    if not ip:
        print("Could not connect to WiFi. Exiting...")
        return

    portfolios_data = fetch_portfolios_data()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", 80))
    s.listen(5)

    print("=" * 50)
    print(f"\n Local server running on http://{ip}:80")
    print(f" Loaded {len(portfolios_data) if portfolios_data else 0} portfolios.")
    print(" Press Ctrl+C to stop the server.\n")
    print("=" * 50)

    try:
        while True:
            conn, addr = s.accept()
            print(f" Connection from {addr}")
            led.on()
            time.sleep(1)

            try:
                request = conn.recv(1024).decode()

                path = parse_request_path(request)
                print(f" Requested path: {path}")

                if path == "/" or path == "":
                    print(" Generating home page...")
                    html_content = generate_home_page(portfolios_data)
                    print(" Serving home page with all portfolios.")
                else:
                    username = path.lstrip("/")
                    portfolio = find_portfolio(portfolios_data, username)

                    if portfolio:
                        html_content = generate_portfolio_html(portfolio)
                        print(f" Serving portfolio for user: {username}")
                    else:
                        html_content = (
                            "<html><body><h1>404 Not Found</h1>"
                            "<p>The requested portfolio does not exist.</p></body></html>"
                        )
                        print(f" Portfolio for user '{username}' not found.")

                http_response = (
                    "HTTP/1.1 200 OK\nContent-Type: text/html\nConnection: close\n\n"
                )
                http_response += html_content
                conn.send(http_response.encode())
            except Exception as e:
                print(f" Error processing request: {e}")
                error_response = "HTTP/1.1 500 Internal Server Error\nContent-Type: text/html\nConnection: close\n\n"
                error_response += (
                    "<html><body><h1>500 Internal Server Error</h1></body></html>"
                )
                conn.send(error_response.encode())
            finally:
                # conn.close() # TODO: Check why closing connection causes issues
                led.off()
                gc.collect()
    except KeyboardInterrupt:
        print("\n Server stopped.")
        led.off()
        s.close()


if __name__ == "__main__":
    start_portfolio_server()
