FROM python:3.12-alpine
# # create and set working directory
WORKDIR /email-backend
# # install dependencies
RUN apk add --no-cache gcc musl-dev linux-headers bash dos2unix
# # copy requirements file
COPY ./requirements.txt requirements.txt
# # install dependencies
RUN pip install --no-cache-dir -r requirements.txt
# # copy project
COPY . .
RUN dos2unix docker-entrypoint.sh && chmod +x docker-entrypoint.sh
CMD ["/bin/bash", "docker-entrypoint.sh"]
