from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import html


PORT = 8000


def page(content):
    return f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>PocketSmart AI</title>

<style>
* {{
    box-sizing:border-box;
}}

body {{
    margin:0;
    font-family:Arial,sans-serif;
    background:#0f172a;
    color:white;
}}

header {{
    background:#1e293b;
    padding:25px;
    text-align:center;
}}

header h1 {{
    margin:0;
    color:#38bdf8;
}}

.container {{
    max-width:650px;
    margin:auto;
    padding:20px;
}}

.card {{
    background:#1e293b;
    padding:25px;
    margin:20px 0;
    border-radius:18px;
}}

input,select {{
    width:100%;
    padding:13px;
    margin:8px 0 18px;
    border-radius:8px;
    border:0;
    font-size:16px;
}}

button {{
    width:100%;
    padding:14px;
    border:0;
    border-radius:8px;
    background:#06b6d4;
    color:white;
    font-size:16px;
    font-weight:bold;
}}

.result {{
    background:#0f766e;
    padding:15px;
    margin:10px 0;
    border-radius:10px;
}}

.back {{
    color:#67e8f9;
}}

h2 {{
    color:#67e8f9;
}}
</style>
</head>

<body>

<header>
<h1>💰 PocketSmart AI</h1>
<p>Smart Budget & Recommendation Assistant</p>
</header>

<div class="container">

{content}

</div>

</body>
</html>
"""


HOME = """
<div class="card">

<h2>🏠 Home Planner</h2>

<form method="POST" action="/home">

<label>Budget ₹</label>
<input type="number" name="budget" required>

<label>Room</label>
<select name="room">
<option>Bedroom</option>
<option>Living Room</option>
<option>Kitchen</option>
<option>Study Room</option>
</select>

<label>Number of Lights</label>
<input type="number" name="lights" value="2">

<label>Number of Fans</label>
<input type="number" name="fans" value="1">

<button>Generate Home Plan</button>

</form>

</div>


<div class="card">

<h2>🎉 Party Planner</h2>

<form method="POST" action="/party">

<label>Budget ₹</label>
<input type="number" name="budget" required>

<label>Guests</label>
<input type="number" name="guests" required>

<label>Event</label>
<select name="event">
<option>Birthday</option>
<option>Wedding</option>
<option>College Event</option>
<option>Family Function</option>
</select>

<button>Generate Party Plan</button>

</form>

</div>


<div class="card">

<h2>💎 Jewelry Planner</h2>

<form method="POST" action="/jewelry">

<label>Budget ₹</label>
<input type="number" name="budget" required>

<label>Occasion</label>
<select name="occasion">
<option>Wedding</option>
<option>Birthday</option>
<option>Festival</option>
<option>Party</option>
<option>Daily Wear</option>
</select>

<label>Style</label>
<select name="style">
<option>Traditional</option>
<option>Modern</option>
<option>Minimal</option>
<option>Bridal</option>
</select>

<button>Generate Jewelry Plan</button>

</form>

</div>
"""


class PocketSmart(BaseHTTPRequestHandler):

    def send_html(self, content):

        data = content.encode("utf-8")

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "text/html; charset=utf-8"
        )

        self.send_header(
            "Content-Length",
            str(len(data))
        )

        self.end_headers()

        self.wfile.write(data)


    def read_form(self):

        length = int(
            self.headers.get("Content-Length", 0)
        )

        body = self.rfile.read(length).decode()

        return parse_qs(body)


    def do_GET(self):

        if self.path == "/":

            self.send_html(
                page(HOME)
            )

        else:

            self.send_response(404)
            self.end_headers()
            self.wfile.write(
                b"404 - Page Not Found"
            )


    def do_POST(self):

        data = self.read_form()

        if self.path == "/home":

            budget = float(
                data.get("budget", ["0"])[0]
            )

            room = html.escape(
                data.get("room", [""])[0]
            )

            lights = int(
                data.get("lights", ["0"])[0]
            )

            fans = int(
                data.get("fans", ["0"])[0]
            )

            light_cost = lights * 500
            fan_cost = fans * 1800
            furniture = budget * 0.50

            total = (
                light_cost
                + fan_cost
                + furniture
            )

            content = f"""

<div class="card">

<h2>🏠 Home Recommendation</h2>

<p>Room: {room}</p>

<div class="result">
💡 Lights: ₹{light_cost:,.0f}
</div>

<div class="result">
🌀 Fans: ₹{fan_cost:,.0f}
</div>

<div class="result">
🛋️ Furniture: ₹{furniture:,.0f}
</div>

<div class="result">
💰 Total: ₹{total:,.0f}
</div>

<p>
Budget: ₹{budget:,.0f}
</p>

<br>

<a class="back" href="/">
← Back
</a>

</div>

"""

            self.send_html(
                page(content)
            )

            return


        if self.path == "/party":

            budget = float(
                data.get("budget", ["0"])[0]
            )

            guests = int(
                data.get("guests", ["0"])[0]
            )

            event = html.escape(
                data.get("event", [""])[0]
            )

            food = budget * 0.50
            decoration = budget * 0.20
            entertainment = budget * 0.15
            venue = budget * 0.15

            content = f"""

<div class="card">

<h2>🎉 Party Recommendation</h2>

<p>Event: {event}</p>

<p>Guests: {guests}</p>

<div class="result">
🍔 Food: ₹{food:,.0f}
</div>

<div class="result">
🎈 Decoration: ₹{decoration:,.0f}
</div>

<div class="result">
🎵 Entertainment: ₹{entertainment:,.0f}
</div>

<div class="result">
🏨 Venue: ₹{venue:,.0f}
</div>

<div class="result">
💰 Total: ₹{budget:,.0f}
</div>

<br>

<a class="back" href="/">
← Back
</a>

</div>

"""

            self.send_html(
                page(content)
            )

            return


        if self.path == "/jewelry":

            budget = float(
                data.get("budget", ["0"])[0]
            )

            occasion = html.escape(
                data.get("occasion", [""])[0]
            )

            style = html.escape(
                data.get("style", [""])[0]
            )

            necklace = budget * 0.45
            earrings = budget * 0.20
            bracelet = budget * 0.15
            ring = budget * 0.10

            content = f"""

<div class="card">

<h2>💎 Jewelry Recommendation</h2>

<p>
Occasion: {occasion}
</p>

<p>
Style: {style}
</p>

<div class="result">
📿 Necklace: ₹{necklace:,.0f}
</div>

<div class="result">
👂 Earrings: ₹{earrings:,.0f}
</div>

<div class="result">
📿 Bracelet: ₹{bracelet:,.0f}
</div>

<div class="result">
💍 Ring: ₹{ring:,.0f}
</div>

<div class="result">
💰 Budget: ₹{budget:,.0f}
</div>

<br>

<a class="back" href="/">
← Back
</a>

</div>

"""

            self.send_html(
                page(content)
            )

            return


        self.send_response(404)
        self.end_headers()


print()
print("=" * 45)
print("       PocketSmart AI")
print("=" * 45)
print()
print("Python:", __import__("sys").version)
print("Server: http://127.0.0.1:8000")
print()
print("No FastAPI")
print("No Pydantic")
print("No Rust")
print("No cryptography")
print("No external packages")
print()
print("=" * 45)

server = HTTPServer(
    ("0.0.0.0", PORT),
    PocketSmart
)

server.serve_forever()
