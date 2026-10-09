import socket  # Used to create a TCP server and handle network communication
import os # Used for working with file paths and directories


#------------------------------------------------
#              SERVER CONFIGURATION
#------------------------------------------------
HOST = '0.0.0.0' # Listen on all network interfaces
PORT = 6501      # Port number for the web server

#------------------------------------------------
#                 LOGGING COUNTERS
#------------------------------------------------
total_requests = 0
success_requests = 0
failed_requests = 0


#BASE DIRECTORY

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Absolute path of project folder
 
# Content-Type headers for different file formats (MIME types)

MIME_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".pdf": "application/pdf",
    ".txt": "text/plain; charset=utf-8"
}

#------------------------------------------------
#               GET CONTENT TYPE
#------------------------------------------------
def get_content_type(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    return MIME_TYPES.get(ext, "application/octet-stream")

# ----------------------------------------------------------
# Build the HTTP response packet to send back to the browser
# ----------------------------------------------------------
def response(status_line, headers, body_bytes):
    response = status_line + "\r\n"
    for key, value in headers.items():
        response += f"{key}: {value}\r\n"
    response += "\r\n"
    return response.encode() + body_bytes

#------------------------------------------------
#               SERVE STATIC FILE
#------------------------------------------------
def serve_file(client_socket, file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError() # file does not exist, trigger 404 handling
    content_type = get_content_type(file_path) # determine file MIME type (html, css, image, etc.)
    with open(file_path, "rb") as file:
        body = file.read() # read file content in binary mode
    headers = {
        "Content-Type": content_type ,  #specify file type for browser
        "Content-Length": str(len(body)), # size of file in bytes
        "Content-Disposition": "inline"  # display file inside browser instead of download
        }

    resp = response( "HTTP/1.1 200 OK", headers,  body)  # build full HTTP response (status + headers + body)

    client_socket.sendall(resp)

#------------------------------------------------
#               SEND ERROR PAGE
#------------------------------------------------
def send_error(client_socket, status_code):

    if status_code == 400: # Bad Request 

        html = f"""
        <html>
        <body>
        <h1>400 Bad Request</h1>
        </body>
        </html>
        """

        status_line = "HTTP/1.1 400 Bad Request"

    elif status_code == 404: # not found 

       html = f"""
        <html>
        <body style="text-align:center;">
        <h1 style="color:red;">404 Not Found</h1>
        <p>Requested file not found</p>
        </body>
        </html>
        """
       status_line = "HTTP/1.1 404 Not Found"

    body = html.encode("utf-8")
    
    headers = {
            "Content-Type": "text/html; charset=utf-8","Content-Length": str(len(body)),"Content-Disposition": "inline"
    }

    resp = response(status_line, headers, body)

    client_socket.sendall(resp)

#------------------------------------------------
#                     LOGGING
#------------------------------------------------
def log(client_addr, path, status):

    global total_requests # keeps track of total number of requests received
    global success_requests  # counts successfully processed requests (200 OK)
    global failed_requests # counts failed requests (400 / 404 errors)

    total_requests += 1 #add number of requests

    if status == 200:
        success_requests += 1
    else:
        failed_requests += 1

    print("\n---------------------------------")
    print("             LOGGING             ")
    print("---------------------------------")

    print("Client IP:", client_addr[0])
    print("Client Port:", client_addr[1])
    print("Requested Path:", path)

    
    print("Status:",status)


    print("Total Requests:", total_requests)
    print("Successful Requests:", success_requests)
    print("Failed Requests:", failed_requests)

    print("---------------------------------")


#------------------------------------------------
#                 SOCKET SETUP
#------------------------------------------------
def setup_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create TCP socket

    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow reuse of port

    server_socket.bind((host, port))# Bind server to host and port

    server_socket.listen(6) # Start listening for connections

    print(f"Server on {host} : {port}") # Show server status


    return server_socket
#------------------------------------------------
#                   MAIN LOOP
#------------------------------------------------
server_socket = setup_server(HOST, PORT)
while True:
    client_socket, client_addr = server_socket.accept() # Accept client connection
    request = client_socket.recv(4096).decode(errors="ignore")# Receive HTTP request
    print("\nREQUEST:\n")
    print(request)
    #------------------------------------------------
    #               PARSE REQUEST
    #------------------------------------------------
    try:
        #first line : Get /path HTTP /1.1
        first_line = request.split("\n")[0] 
        parts = first_line.split()
        if len(parts) != 3:
            raise Exception("400")
        method = parts[0] # HTTP method (GET)
        path = parts[1]  # Requested path
    except:
        send_error(client_socket, 400)
        log(client_addr, "UNKNOWN", 400)
        client_socket.close()  # Close connection
        continue
    #------------------------------------------------
    #                 ONLY GET
    #------------------------------------------------
    if method != "GET":
        send_error(client_socket, 400)
        log(client_addr, path, 400)
        client_socket.close()
        continue
    #------------------------------------------------
    #               REMOVE QUERY
    #------------------------------------------------
    path = path.split("?")[0]
    #------------------------------------------------
#                   ROUTING
#------------------------------------------------
    if path in ("/", "/en", "/home_en.html", "/index.html"): # English homepage
        filename = os.path.join("html", "home_en.html")
    elif path in ("/ar", "/home_ar.html"):
        filename = os.path.join("html", "home_ar.html")  # Arabic homepage

    elif path.startswith("/imgs/"): # Image files path
        filename = path.lstrip("/")
    else:
        filename = path.lstrip("/")
    file_path = os.path.join(BASE_DIR, filename)# Full file path

    try:

        serve_file(client_socket, file_path)
        status = 200          #  SERVE FILE
    except:
        send_error(client_socket, 404)
        status = 404 # FILE NOT FOUND
    #------------------------------------------------
    #                    LOGGING
    #------------------------------------------------
    log(client_addr, path, status)

    client_socket.close()# Close client connection