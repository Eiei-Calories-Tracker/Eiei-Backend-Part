# Set up Part

## 1 Install Python 3.11 Virtual Environment (Window)

```
python3.11 -m venv venv
py -3.11 -m venv venv
venv\Scripts\Activate.ps1
```

## 2 Pip install (Please Ensure You are in VENV)

```
pip install -r requirements.txt
```

## 3 Attach .env at root directory

## 4 (First Time) Install ngrok (For now) and set up your domain and also your auth token

```
https://ngrok.com/download/windows?tab=install_scoop
```

# Running Part

## 5 Run with cd to app directory

```
python main.py
```

## 6 Run ngrok to connect your backend

```
ngrok http [YOUR_PORT]
```
