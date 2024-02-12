FROM manimcommunity/manim:v0.18.0

# Use root for installation processes
USER root

# Install Jupyter Notebook without using cache
RUN pip install notebook

# Copy requirements.txt file
COPY requirements.txt /tmp/

# Display the contents of requirements.txt
RUN cat /tmp/requirements.txt

# Install dependencies from requirements.txt file without using cache
RUN pip install -r /tmp/requirements.txt

COPY . /dsa-book.github.io

WORKDIR /dsa-book.github.io/docs

ARG NB_USER=manimuser

USER ${NB_USER}

COPY --chown=manimuser:manimuser . /dsa-book.github.io


