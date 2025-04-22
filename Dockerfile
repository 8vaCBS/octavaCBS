FROM mcr.microsoft.com/playwright/python:v1.41.2-jammy

WORKDIR /app

COPY extractor_estado_playwright.py ./
COPY requirements.txt ./

RUN pip install -r requirements.txt

# Este comando instala los navegadores de Playwright
RUN playwright install --with-deps

CMD ["python", "extractor_estado_playwright.py"]
