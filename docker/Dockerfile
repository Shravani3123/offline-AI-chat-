# Step 1: Use Python as the base image
FROM python:3.10

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy chatbot files into the container
COPY ../app /app/app
COPY ../bot /app/bot
COPY ../requirements.txt /app/

# Step 4: Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Run the chatbot script (change if needed)
CMD ["python", "app/app.py"]
