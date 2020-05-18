FROM python:3

RUN apt-get update && apt-get install -y cmake

WORKDIR /usr/src/app

ENV DB_PATH="sqlite:///data/updater.db"
ENV MAPPING_PATH="data/inara_commodities_map.csv"

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "-m", "server" ]