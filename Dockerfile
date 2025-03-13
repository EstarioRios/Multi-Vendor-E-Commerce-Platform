# Use the official Python 3.10 base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy required files into the container
COPY requirements.txt .
COPY manage.py .
COPY MVP/ MVP/
COPY AuthenticationSystem/ AuthenticationSystem/
COPY Product/ Product/

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Grant necessary permissions to the manage.py file
RUN chmod +x manage.py

# Expose port 8000 to allow access to the Django server
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
