FROM mysql:8.0-debian

RUN apt update
RUN apt install python3-pip -y

WORKDIR /dwh

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt --break-system-packages

COPY . .

