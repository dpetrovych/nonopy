FROM python:3.8-slim

WORKDIR /usr/app
ADD nonopy ./nonopy
ADD cli.py requirements.txt ./

RUN python -m pip install -r requirements.txt

ENTRYPOINT [ "python", "cli.py" ]
