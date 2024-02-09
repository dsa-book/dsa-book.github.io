FROM manimcommunity/manim:v0.18.0

# Switch to root to install additional dependencies
USER root

# Install Jupyter Notebook (or JupyterLab if preferred)
RUN pip install notebook

RUN ls /tmp/

# Install dependencies from requirements.txt file
# Ensure your requirements.txt file is in the build context
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

# Setup argument for non-root user
ARG NB_USER=manimuser

# Switch back to the non-root user for running the application
USER ${NB_USER}

# Copy your application code (with proper ownership)
COPY --chown=manimuser:manimuser . /manim
