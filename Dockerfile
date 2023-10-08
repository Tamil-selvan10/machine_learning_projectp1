FROM python:3.8
COPY . /app 
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE $PORT 
CMD gunicorn --workers=4 --bind 0.0.0.0:$PORT app:app

# COPY . /app     ,. -> current directory all files and folders except file and folders mentioned in the .dockerignore file.
# EXPOSE $PORT    ,Declare a variable PORT