import asyncio
from playwright.async_api import async_playwright

async def main():
    url = "https://icbs.cl/c/v/985"
    output_file = "estado_carros_actualizado.html"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")

        # Espera explícita por el contenedor de los carros
        await page.wait_for_selector("div.row.servicio")

        content = await page.content()

        # Guardamos el contenido completo como respaldo
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())