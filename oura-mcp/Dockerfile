FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py server_http.py ./

# The host platform provides $PORT; server_http.py binds 0.0.0.0:$PORT.
# OURA_PERSONAL_ACCESS_TOKEN and OURA_MCP_SECRET are supplied as env vars.
CMD ["python", "server_http.py"]
