# FROM ubuntu:20.04

# # Combine update, install, and cleanup in one command to reduce image size
# RUN apt-get update -y && \
#     apt-get install python3-pip -y && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/*

# # Copy only the requirements.txt initially to leverage Docker cache
# COPY requirements.txt /opt/requirements.txt

# # Install Python dependencies, including gunicorn
# RUN pip3 install --no-cache-dir --upgrade pip && \
#     pip3 install --no-cache-dir gunicorn && \
#     pip3 install --no-cache-dir -r /opt/requirements.txt

# # Copy the rest of the application
# COPY . /opt/

# WORKDIR /opt/

# # Use the gunicorn command, not gunicorn3
# CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app", "--workers=5"]



# FROM python:alpine
# Use the Python3.7.2 image
# 指定一個 image 來源
FROM python:3.8-slim

RUN apt-get update -y && \
    apt-get install python3-pip -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
# Set the working directory to /app

WORKDIR /app

# Copy the current directory contents into the container at /app 
# ADD：將檔案加到 images 內
ADD . /app

COPY requirements.txt /opt/requirements.txt

# Install the dependencies
# build 時使用，會執行此命令
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir --upgrade pip
RUN pip3 install -r requirements.txt

# run the command to start uWSGI
# run container 時要執行的命令
CMD ["uwsgi", "app.ini"]


# ENV：環境變數設定