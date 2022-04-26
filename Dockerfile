FROM python:3

EXPOSE 8095

RUN apt-get update
RUN apt-get install -y bluez bluetooth bluez-hcidump ghostscript
RUN pip install bleak

WORKDIR /usr/app/src
COPY . .

RUN chmod +x entrypoint.sh

RUN echo "before entrypoint"

ENTRYPOINT sh entrypoint.sh
