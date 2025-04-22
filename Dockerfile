FROM mcr.microsoft.com/playwright/python:v1.41.2-jammy

WORKDIR /app
COPY extractor_estado_playwright.py ./
RUN playwright install --with-deps

CMD ["python", "extractor_estado_playwright.py"]
