FROM python:3.9.7-slim-bullseye

# optional line
WORKDIR /usr/src/app

# copy reqirements in current working directory
COPY requirements.txt ./

# install requirements 
RUN pip install --no-cache-dir -r requirements.txt

# copy all from current dir to current work dir in image
COPY . .

# command to run when we run containers

CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]

