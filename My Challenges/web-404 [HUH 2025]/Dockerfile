FROM python:3.11-slim

WORKDIR /app
RUN useradd --create-home --shell /bin/false ctfuser

COPY server.py /app/

RUN pip install --no-cache-dir Flask gunicorn
RUN chown -R ctfuser:ctfuser /app
USER ctfuser

EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "server:app", "--workers", "3", "--threads", "2"]