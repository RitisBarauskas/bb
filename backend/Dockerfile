FROM python:3.9
WORKDIR /code
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . .
CMD gunicorn bb.wsgi:application --bind 0.0.0.0:8000