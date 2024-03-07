# Use an official Python runtime as a parent image
FROM --platform=linux/amd64 python

# Set the working directory in the container
WORKDIR /usr/src/app

#DEFINE ENV VARS
ENV WEATHER_API_KEY=WEATHER_API_KEY
ENV OPENAI_API_KEY=OPENAI_API_KEY
ENV VESTABOARD_API_KEY=VESTABOARD_API_KEY
ENV VESTABOARD_IP_ADDRESS=VESTABOARD_IP_ADDRESS
ENV ZIP_CODE=ZIP_CODE

# Copy the current directory contents into the container
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install cron
RUN apt-get update && apt-get -y install cron nano 

# Add crontab file in the cron directory
ADD crontab /etc/cron.d/weather-cron

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh

# Make sript executable
RUN chmod +x /entrypoint.sh

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/weather-cron

# Apply cron job
RUN crontab /etc/cron.d/weather-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Set the entrypoint
ENTRYPOINT ["/entrypoint.sh"]