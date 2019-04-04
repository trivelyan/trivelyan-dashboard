# triveltan-docker-file
# github.com/tlhcelik
# github.com/trivelyan
# trivelyan.github.io
# licensed by AGPLv3 

FROM python:2.7
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
