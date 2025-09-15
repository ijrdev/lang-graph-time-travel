FROM python:3.10

ENV TZ=America/Recife

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN python -m pip install --upgrade pip
RUN apt-get update && apt-get install -y \
    curl \
    apt-transport-https \
    unixodbc \
    unixodbc-dev \
    gnupg2 \
    software-properties-common

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

COPY ./ app/
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "app.py"]