# Stage 1: Build stage
FROM node:14-alpine as build

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install sass
RUN npm install -g sass

# Compile SASS to CSS
RUN sass static/sass/styles.scss static/css/styles.css

# Stage 2: Final stage
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the compiled CSS from the build stage
COPY --from=build /app/static/css /app/static/css

# Copy the rest of the app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir Flask psutil

# Make port 5000 available to the world outside this container
EXPOSE 5001

# Define environment variable Just for testing rightnow
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]
