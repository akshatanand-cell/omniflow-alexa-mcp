import asyncio
import os
import sys
from playwright.async_api import async_playwright

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "live_captures")
os.makedirs(OUTPUT_DIR, exist_ok=True)

TARGET_URL = "https://omniflow-alexa-mcp.vercel.app/"

async def capture():
    print(f"🌐 Launching Chromium to capture live deployment: {TARGET_URL}...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Standard 1080p display viewport
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})

        # 1. Initial State
        print("  📸 Capturing 1: Initial Alexa+ Ambient Home State...")
        await page.goto(TARGET_URL, wait_until="networkidle")
        await asyncio.sleep(2)
        await page.screenshot(path=os.path.join(OUTPUT_DIR, "live_01_home.png"))

        # 2. Trigger Autonomous Goal Execution
        print("  🚀 Clicking sample prompt: '3-Day Olympic NP Trip under $300'...")
        # Click the first sample chip
        chips = page.locator(".sample-chip")
        await chips.first.click()

        # Wait for agent execution and cards to appear
        print("  ⏳ Waiting for Bedrock Agent & MCP tools to execute...")
        await page.wait_for_selector("#orderActionCard", timeout=20000)
        await asyncio.sleep(2)

        # 3. Full Multi-Modal Screen State
        print("  📸 Capturing 2: Multi-Modal Itinerary & Prime Carousel...")
        await page.screenshot(path=os.path.join(OUTPUT_DIR, "live_02_results.png"))

        # 4. Scroll down slightly to showcase the budget progress & order card
        print("  📸 Capturing 3: Budget Optimization & Order Card...")
        await page.evaluate("window.scrollBy(0, 320)")
        await asyncio.sleep(1)
        await page.screenshot(path=os.path.join(OUTPUT_DIR, "live_03_budget_cart.png"))

        # 5. Open MCP Protocol Inspector
        print("  📸 Capturing 4: Live MCP Protocol Inspector (Streamable HTTP)...")
        await page.locator("#toggleInspectorBtn").click()
        await asyncio.sleep(1.5)
        await page.screenshot(path=os.path.join(OUTPUT_DIR, "live_04_mcp_inspector.png"))

        # 6. Click Confirm Order (Human-in-the-loop Guardrail Trigger)
        print("  📸 Capturing 5: Order Confirmation Guardrail Execution...")
        await page.locator("#closeInspectorBtn").click()
        await asyncio.sleep(0.5)
        confirm_btn = page.locator("#confirmOrderBtn")
        if await confirm_btn.is_visible():
            await confirm_btn.click()
            await asyncio.sleep(2)
        await page.screenshot(path=os.path.join(OUTPUT_DIR, "live_05_order_confirmed.png"))

        await browser.close()
        print("✅ All live screenshots successfully captured from Vercel!")

if __name__ == "__main__":
    asyncio.run(capture())
