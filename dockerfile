# Use an appropriate base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Install git
RUN apt-get update && apt-get install -y git

# Clone the repository
RUN git clone -b main https://github.com/V4Cmeister/MCI_IoT_Monitor3D.git .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure start.sh is executable
RUN chmod +x start.sh

# Set the entry point
CMD ["./start.sh"]
