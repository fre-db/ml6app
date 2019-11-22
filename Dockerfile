FROM python:3.5

RUN mkdir /ml6app
WORKDIR /ml6app
ADD . /ml6app/

RUN pip install -r /ml6app/requirements.txt



ENV PORT 8080
CMD ["python", "/ml6app/app.py"]