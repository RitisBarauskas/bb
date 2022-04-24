FROM python:3.9
WORKDIR /tgbot
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . .
ENTRYPOINT ["python", "app.py"]