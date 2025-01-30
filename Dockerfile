# Start from an official Python base image
FROM python:3.11-slim

# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /usr/share/keyrings/google-chrome-keyring.gpg \
    && echo 'deb [signed-by=/usr/share/keyrings/google-chrome-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Get the latest Chrome WebDriver version compatible with the installed Chrome
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}') \
    && DRIVER_VERSION=$(curl -sS https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json | \
    python3 -c "import sys, json; data=json.load(sys.stdin); print(next(v['version'] for v in data['versions'] if v['version'].startswith('$CHROME_VERSION')))") \
    && DRIVER_URL="https://storage.googleapis.com/chrome-for-testing-public/$DRIVER_VERSION/linux64/chromedriver-linux64.zip" \
    && wget -q $DRIVER_URL -O /tmp/chromedriver.zip \
    && unzip /tmp/chromedriver.zip -d /tmp/ \
    && mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf /tmp/chromedriver.zip /tmp/chromedriver-linux64

# Install Selenium
RUN pip install --no-cache-dir selenium

# Set working directory
#WORKDIR /app

# Copy project files (if applicable)
#COPY . .

# Set default command
#CMD ["python", "example_result.py" ]
