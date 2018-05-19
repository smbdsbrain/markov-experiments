FROM python:3.6

ARG APP_DIR=/app
WORKDIR "$APP_DIR"

COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --system
ENV PYTHONPATH $APP_DIR

COPY . $APP_DIR/

ENTRYPOINT ["sh", "entrypoint.sh"]
