# Python installation packaged with Debian12
FROM python:3.11-slim


# Set environment variables (from https://docs.python.org/3/using/cmdline.html)
# - PYTHONDONTWRITEBYTECODE:
#     - If this is set to a non-empty string, Python won't try to write .pyc files on the import of 
#       source modules. 
# - PYTHONUNBUFFERED:
#     - If this is set to a non-empty string, force the stdout and stderr streams to be unbuffered. 
#       This option has no effect on the stdin stream.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /app

COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

EXPOSE 8000

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]