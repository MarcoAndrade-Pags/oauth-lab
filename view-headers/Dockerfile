# start by pulling the python image
FROM python:3.8-alpine

# switch working directory
WORKDIR /app

# copy the requirements file into the image
COPY ./requirements.txt view.py .


RUN chmod a+x /app/view.py

# install the dependencies and packages in the requirements file
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r /app/requirements.txt


# copy every content from the local file to the image
COPY . /app

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["view.py" ]
