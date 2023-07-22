
FROM python:3.10

# Set the working directory, add the current directory contents into the container at /app, and install packages
WORKDIR /app
ADD . /app
RUN pip install --no-cache-dir -r requirements.txt

# Run the command to start uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
