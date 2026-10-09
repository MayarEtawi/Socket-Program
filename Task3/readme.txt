Simple File-Sharing Web Server

Folder Structure:

Task3/
server.py
readme.txt

html/
- home_en.html
- home_ar.html

css/
- style.css

imgs/
- Hala.jpg
- Mayar.jpg
- Maryam.jpg

files/
- nn.pdf
- readme.txt
- sample.html

Description:
This project implements a simple file-sharing web server using Python socket programming and HTTP communication. The server handles HTTP GET requests, serves HTML pages, CSS files, images, and downloadable files, and supports HTTP response codes such as 200 OK, 400 Bad Request, and 404 Not Found.

Port Number:
6501

Supported URLs:
- /
- /en
- /index.html
- /home_en.html
- /ar
- /home_ar.html

How to Run:
1. Open a terminal inside the Task3 folder.
2. Run:
   python server.py
3. Open a web browser.
4. Access:
   http://localhost:6501

Requirements:
- Python 3.x
- Web browser