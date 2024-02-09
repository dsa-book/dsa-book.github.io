FROM manimcommunity/manim:v0.18.0

USER root
RUN pip install notebook
RUN pip install -r requirements.txt

ARG NB_USER=manimuser
USER ${NB_USER}

COPY --chown=manimuser:manimuser . /manim
