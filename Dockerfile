FROM python:3.5

RUN mkdir /ml6app
WORKDIR /ml6app
ADD . /ml6app/

RUN pip install -r /ml6app/requirements.txt



EXPOSE 5000
CMD ["python", "/ml6app/app.py"]