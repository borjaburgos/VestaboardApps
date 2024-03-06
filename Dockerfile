# Use an official Python runtime as a parent image
FROM --platform=linux/amd64 python

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install cron
RUN apt-get update && apt-get -y install cron

# Add crontab file in the cron directory
ADD crontab /etc/cron.d/weather-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/weather-cron

# Apply cron job
RUN crontab /etc/cron.d/weather-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log
