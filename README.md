# CodeAlpha Task 1 - Simple URL Shortener

This project is made for the CodeAlpha Backend Development Task 1.

## Features
- Flask backend server
- POST API endpoint: `/api/shorten`
- Generates a unique short code
- Stores original URLs and short codes in SQLite
- Redirects short URLs to the original URL
- Simple browser interface

## Run

### Windows
Open Command Prompt in this folder and run:

```bat
pip install -r requirements.txt
python app.py
```

Then open:

http://127.0.0.1:5000

## API example

POST `/api/shorten`

JSON:
```json
{
  "url": "https://www.google.com"
}
```

Example response:
```json
{
  "original_url": "https://www.google.com",
  "short_code": "aB12xY",
  "short_url": "http://127.0.0.1:5000/aB12xY"
}
```

## GitHub
Create a repository named:

`CodeAlpha_ProjectName`

Upload all project files.
