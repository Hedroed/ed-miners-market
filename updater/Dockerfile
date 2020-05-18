FROM python:3-slim

# RUN apt-get update && apt-get install -y cmake

WORKDIR /usr/src/app

ENV DB_PATH="sqlite:///data/updater.db"

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "updater.py" ]