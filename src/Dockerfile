FROM python:3
ARG APP_USER_NAME='nori'

WORKDIR /home/$APP_USER_NAME

RUN mkdir -p /home/${APP_USER_NAME}/ffmpeg
RUN mkdir -p /home/${APP_USER_NAME}/x264
RUN mkdir -p /home/${APP_USER_NAME}/x265

COPY ./execute.py /home/$APP_USER_NAME/
COPY ./id.py /home/$APP_USER_NAME/
COPY ./util.py /home/$APP_USER_NAME/
COPY ./settings.py /home/$APP_USER_NAME/
COPY ./requirements.txt /home/$APP_USER_NAME/
COPY ./rewrite_pafy.sh /home/$APP_USER_NAME/

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN apt-get install -y vim less
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt
RUN pip install git+https://github.com/mps-youtube/pafy.git@develop

RUN apt-get -y install ffmpeg
COPY --from=ajekadier/x264 / /home/$APP_USER_NAME/x264
COPY --from=louisliu/x265 / /home/$APP_USER_NAME/x265

ENTRYPOINT [ "python3", "execute.py" ]
