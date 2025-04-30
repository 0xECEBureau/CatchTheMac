"""Headless admin bot that periodically visits the main page with admin cookies.
This simulates the administrator reading the chat, enabling XSS exploitation.
"""
import asyncio, os
from pyppeteer import launch

TARGET = os.getenv("TARGET", "http://localhost:5000/")
INTERVAL = int(os.getenv("INTERVAL", "15"))

# Cookies donnés au bot (admin + flag)
COOKIES = [
    {"name": "role", "value": "YWRtaW4=", "domain": "localhost"},  # "admin" base64
    {"name": "flag", "value": "MAC{L4Y3R5_6_7_XSS_m4st3r}", "domain": "localhost"},
]

async def browse_once():
    browser = await launch(headless=True, args=[
        "--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage",
        "--disable-gpu", "--disable-3d-apis", "--disable-dev-tools"],
        executablePath="/usr/bin/chromium")
    page = await browser.newPage()
    await page.setCookie(*COOKIES)
    await page.goto(TARGET, timeout=60000)
    await asyncio.sleep(5)  # laisser tourner les scripts XSS
    await browser.close()

async def loop_forever():
    while True:
        try:
            await browse_once()
        except Exception as e:
            print("[bot] Error:", e)
        await asyncio.sleep(INTERVAL)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(loop_forever())