FROM python:3.9
#ENV FLASK_APP=view.py
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN python3 check_db.py
EXPOSE 9999
CMD ["python3", "/app/views.py"]
