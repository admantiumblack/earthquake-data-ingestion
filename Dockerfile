FROM python:3.12-alpine as test
RUN apk update
WORKDIR /app
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY ./ ./
ENTRYPOINT ["pytest", "."]
CMD ["--doctest-modules", "--junitxml=junit/test-results.xml", "--cov=.", "--cov-report=xml", "--cov-report=html"]

FROM python:3.12-alpine as build
RUN apk update && apk add binutils
WORKDIR /app
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
RUN pip install pyinstaller
COPY ./ ./
RUN pyinstaller main.py -n ingest_earthquake --onefile

FROM alpine as deploy
COPY --from=build /app/dist/ingest_earthquake ./ingest_earthquake
COPY --from=build /app/extraction/api_sources/ ./extraction/api_sources/
RUN chmod +x ingest_earthquake
ENV STORAGE_LOCATION=localhost
ENTRYPOINT ["./ingest_earthquake"]
CMD []