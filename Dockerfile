FROM manimcommunity/manim:v0.18.0

# Use root for installation processes
USER root

# Install Jupyter Notebook without using cache
RUN pip install --upgrade pip
RUN pip install --no-cache-dir notebook

# Copy requirements.txt file
COPY requirements.txt /tmp/

# Display the contents of requirements.txt
RUN cat /tmp/requirements.txt

# Install dependencies from requirements.txt file without using cache
RUN pip install --no-cache-dir -r /tmp/requirements.txt

ARG NB_USER=manimuser

# Switch back to the non-root user for running the application
USER ${NB_USER}

# Copy your application code with the correct ownership
COPY --chown=manimuser:manimuser . /manim
