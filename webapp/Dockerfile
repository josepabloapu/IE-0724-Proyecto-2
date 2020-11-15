# Base Image
FROM python:3.8-buster

# Docker image info
LABEL mantainer="MARLON_LAZO_Y_JOSE_APU"
LABEL version="1.0"
LABEL description="App Web para registro de propiedades"

# Create and set working directory
WORKDIR /webapp
ADD . /webapp

# Set defautl environment variables
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

# Define timezone
ENV TZ=America/Costa_Rica
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
	&& echo $TZ > /etc/timezone

# Add scripts folder
ENV PATH="/webapp:${PATH}"
RUN chmod +x entrypoint.sh

# Add python requirements
RUN pip install -r requirements.txt

# Create a user for the project
RUN adduser --disabled-password --gecos '' user

# Add static folders
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN chown -R user:user /vol
RUN chmod -R 755 /vol/web

# Switch users
USER user

# Run server
CMD ["entrypoint.sh"]
