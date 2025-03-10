# Python image to use.
FROM python:3.10

# Expose 8501 as the port
EXPOSE 8501

# Set the working directory to /app
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
# Copy the directory contents into the container
COPY . ./

# Install any needed packages specified in requirements.txt

# The main command to run when the container starts.
ENTRYPOINT ["streamlit", "run", "app.py"]
