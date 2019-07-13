FROM python:3-alpine

ADD ./listthedocs/ ./listthedocs/
ADD ./MANIFEST.in ./MANIFEST.in
ADD ./setup.py ./setup.py

ENV HTD_HOST "0.0.0.0"
ENV HTD_PORT 5000

EXPOSE 5000

CMD [ "python", "runserver.py" ]
