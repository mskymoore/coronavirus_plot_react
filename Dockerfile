FROM python:3.8
ENV PYTHONUNBUFFERED=1
RUN mkdir /opt/coronavirus_plot_web
WORKDIR /opt/coronavirus_plot_web
COPY ./requirements.txt /opt/coronavirus_plot_web/requirements.txt
RUN pip install -r ./requirements.txt
