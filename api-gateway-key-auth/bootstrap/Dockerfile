# start by pulling the python image
FROM hashicorp/vault:latest

# switch working directory
WORKDIR /app

# copy the requirements file into the image
COPY bootstrap.sh /app
#COPY ../config/kong+service+key.yaml .

RUN chmod a+x /app/bootstrap.sh
RUN printenv

ENTRYPOINT [ "/app/bootstrap.sh" ]

