FROM python:3.8

ARG GROUP_ID=1000
ARG USER_ID=1000

RUN echo "group_id $GROUP_ID"
RUN echo "user_id $USER_ID"

RUN addgroup --gid $GROUP_ID app && adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID app

RUN mkdir -p /app/media /app/static \
    && chown -R app:app /app/

RUN apt-get update && \
    apt-get install -y gettext-base gettext

COPY ./requirements.txt /app/

RUN pip install --upgrade pip && pip install -r /app/requirements.txt

COPY ./docker/app/gunicorn.conf.py /gunicorn.conf.py

COPY . /app/

WORKDIR /app

RUN chown -R app:app /app

USER app

EXPOSE 8000

CMD gunicorn -c /gunicorn.conf.py --log-level=${DJANGO_LOGLEVEL}--max-requests=1000 --access-logfile - --error-logfile - --bind=0.0.0.0:8000 app.wsgi:application
