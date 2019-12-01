FROM python:3.6

RUN mkdir /ml6app
WORKDIR /ml6app
ADD . /ml6app/

RUN apt-get update && apt-get install -y --no-install-recommends libsndfile1
RUN pip install -r /ml6app/requirements.txt

ENV PORT 8080
CMD ["gunicorn", "app:app", "--workers 2", "--threads 2", "-k gthread"]