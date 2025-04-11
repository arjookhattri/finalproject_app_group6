# Dockerfile for Flask App with Ubuntu Base and Port 81

FROM ubuntu:20.04

# Install dependencies and MySQL client
RUN apt-get update -y \
    && apt-get install -y python3-pip python3-dev \
    && apt-get install -y mysql-client \
    && apt-get clean

# Copy application files
COPY . /app
WORKDIR /app


# Install Python dependencies
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Ensure static directory exists (for S3 downloaded images)
RUN mkdir -p /app/static 


# Expose the required port
EXPOSE 81

# Run the application
ENTRYPOINT ["python3"]
CMD ["app.py"]
