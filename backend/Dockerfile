FROM python:3.9
WORKDIR /code
RUN python -m pip install --upgrade pip
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
CMD gunicorn bb.wsgi:application --bind 0.0.0.0:8000