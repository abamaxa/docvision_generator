# Use an official Python runtime as a parent image
FROM python:3.6-slim

WORKDIR /question_factory

# Copy the current directory contents into the container at /app
ADD . /question_factory

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME QuestionFactory

# Run app.py when the container launches
CMD ["python", "question_factory.py", "-p 0", "10"]
