FROM python:3.12 as test
RUN apt-get update && apt-get upgrade
WORKDIR /app
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY ./ ./
ENTRYPOINT ["pytest", "."]
CMD ["--doctest-modules", "--junitxml=junit/test-results.xml", "--cov=.", "--cov-report=xml", "--cov-report=html"]

FROM python:3.12 as build
RUN apt-get update && apt-get upgrade
WORKDIR /app
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY ./ ./
RUN chmod +x ./main.py
ENTRYPOINT ["python", "./main.py"]
CMD []
