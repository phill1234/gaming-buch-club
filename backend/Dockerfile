FROM python:3.12-slim

RUN ln -s /usr/local/bin/python /bin/python
RUN pip install poetry

WORKDIR /app
ADD pyproject.toml pyproject.toml
ADD poetry.lock poetry.lock
RUN poetry install --without dev

ADD . .

EXPOSE 8000

CMD ./make.sh run