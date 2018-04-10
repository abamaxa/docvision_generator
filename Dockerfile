# Use an official Python runtime as a parent image
FROM python:3.6

WORKDIR /doc_vision_synth

# Copy the current directory contents into the container at /app
ADD requirements.txt /doc_vision_synth

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN apt-get update && apt-get install -y texlive-latex-base dvipng

# Copy the current directory contents into the container at /app
ADD . /doc_vision_synth

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
ENTRYPOINT ["python", "main.py"]
CMD ["--help"]
