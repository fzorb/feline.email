FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y git
RUN git clone https://github.com/fzorb/feline.email.git .

RUN pip install -r requirements.txt

EXPOSE 8080

ENV FLASK_APP=feline.email
ENV FLASK_ENV=production

CMD ["waitress-serve", "--call", "feline.email:create_app"]
