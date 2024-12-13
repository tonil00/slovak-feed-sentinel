# Use an official Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the project files to the container
COPY . /app

# Install Poetry
RUN pip install poetry

# Install project dependencies
RUN poetry install --no-dev

# Set the default command to run the project
CMD ["poetry", "run", "python", "slovak_feed_sentinel/rss_catcher.py"]
