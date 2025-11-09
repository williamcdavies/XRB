# Python installation packaged with Debian12
FROM python:3.11.2-slim
 
WORKDIR /app
 
# Set environment variables (from https://docs.python.org/3/using/cmdline.html)
# - PYTHONDONTWRITEBYTECODE:
#     - If this is set to a non-empty string, Python won't try to write .pyc files on the import of 
#       source modules. 
# - PYTHONUNBUFFERED:
#     - If this is set to a non-empty string, force the stdout and stderr streams to be unbuffered. 
#       This option has no effect on the stdin stream.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
 
RUN pip install --upgrade pip 
 
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt
 
COPY . /app/
RUN chmod +x /app/entrypoint.sh
 
EXPOSE 8080

ENTRYPOINT ["/app/entrypoint.sh"]