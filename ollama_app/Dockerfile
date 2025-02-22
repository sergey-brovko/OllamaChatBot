FROM python:3.12


WORKDIR /code


COPY ./requirements.txt /code/


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./main.py /code/


CMD ["python", "main.py"]