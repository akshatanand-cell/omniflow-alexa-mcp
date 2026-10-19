import asyncio
import os
import sys
from playwright.async_api import async_playwright

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = os.path.join(os.path.dirname(__file__), "..")
OUTPUT_PDF = os.path.join(ROOT_DIR, "OmniFlow_Executive_Whitepaper.pdf")

HTML_CONTENT = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8"/>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    body {
      font-family: 'Inter', -apple-system, sans-serif;
      color: #0f172a;
      line-height: 1.5;
      margin: 0;
      padding: 40px;
      font-size: 13px;
    }
    .header {
      border-bottom: 3px solid #00a8e1;
      padding-bottom: 20px;
      margin-bottom: 25px;
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
    }
    .title {
      font-size: 26px;
      font-weight: 800;
      color: #0369a1;
      margin: 0;
    }
    .subtitle {
      font-size: 14px;
      color: #64748b;
      margin-top: 4px;
      font-weight: 500;
    }
    .badge {
      background: #e0f2fe;
      color: #0369a1;
      font-weight: 700;
      padding: 6px 14px;
      border-radius: 9999px;
      font-size: 11px;
      border: 1px solid #bae6fd;
    }
    h2 {
      font-size: 16px;
      font-weight: 700;
      color: #0f172a;
      border-left: 4px solid #00a8e1;
      padding-left: 10px;
      margin-top: 25px;
      margin-bottom: 12px;
    }
    p, li {
      color: #334155;
    }
    ul {
      margin-top: 6px;
      padding-left: 20px;
    }
    li {
      margin-bottom: 5px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 10px;
      margin-bottom: 15px;
    }
    th, td {
      border: 1px solid #cbd5e1;
      padding: 8px 12px;
      text-align: left;
      font-size: 12px;
    }
    th {
      background-color: #f1f5f9;
      font-weight: 700;
      color: #1e293b;
    }
    .highlight-box {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      padding: 14px;
      margin: 15px 0;
    }
    .grid-2 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 15px;
    }
    .card {
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      padding: 12px;
      background: #fafafa;
    }
    .footer {
      margin-top: 40px;
      border-top: 1px solid #e2e8f0;
      padding-top: 15px;
      font-size: 11px;
      color: #94a3b8;
      display: flex;
      justify-content: space-between;
    }
  </style>
</head>
<body>

  <div class="header">
    <div>
      <h1 class="title">OmniFlow</h1>
      <div class="subtitle">Agentic Alexa+ Life & Commerce Copilot • Technical Architecture & Submission Whitepaper</div>
    </div>
    <div class="badge">Amazon Developer Hackathon 2026</div>
  </div>

  <div class="highlight-box">
    <strong>Executive Summary:</strong> OmniFlow is an autonomous, multi-modal Alexa+ Agent Skill and self-hosted Model Context Protocol (MCP) server compliant with MCP specification version <strong>2025-11-25 over Streamable HTTP</strong>, integrated with <strong>Amazon Bedrock (Claude 3.5 Sonnet)</strong>. It transitions digital assistants from single-turn reactive bots into proactive, goal-driven orchestrators capable of resolving high-level complex tasks across services with deterministic safety guardrails.
  </div>

  <h2>1. Primary Track & Challenge Alignments</h2>
  <table>
    <tr>
      <th>Category</th>
      <th>Specification / Target</th>
      <th>Implementation Details</th>
    </tr>
    <tr>
      <td><strong>Primary Track</strong></td>
      <td>Alexa+ Agent Skill & MCP Server</td>
      <td>Fully compliant with MCP 2025-11-25 over Streamable HTTP (SSE); multi-modal visual cards on Echo Show & Web Simulator.</td>
    </tr>
    <tr>
      <td><strong>Mini-Challenge 1</strong></td>
      <td>AWS Builder Mini Challenge</td>
      <td>Integrated Amazon Bedrock Runtime SDK (<code>@aws-sdk/client-bedrock-runtime</code>) with Claude 3.5 Sonnet Converse API function calling.</td>
    </tr>
    <tr>
      <td><strong>Mini-Challenge 2</strong></td>
      <td>Open Source Mini Challenge</td>
      <td>100% open-source under MIT License at <code>https://github.com/akshatanand-cell/omniflow-alexa-mcp</code>.</td>
    </tr>
    <tr>
      <td><strong>Bonus Points</strong></td>
      <td>Product Feedback & Friction Log (+10%)</td>
      <td>Comprehensive friction log covering Streamable HTTP SSE header negotiation and Bedrock schema validation in <code>docs/FRICTION_LOG.md</code>.</td>
    </tr>
  </table>

  <h2>2. System Architecture & Model Context Protocol Tools</h2>
  <p>OmniFlow exposes four atomic tools conforming to JSON-Schema parameters exported directly via standard JSON-RPC 2.0 endpoints:</p>
  <ul>
    <li><strong><code>plan_itinerary</code></strong>: Formulates comprehensive multi-day trip schedules, activities, outdoor locations, and weather forecasts.</li>
    <li><strong><code>search_amazon_products</code></strong>: Live product search querying Prime-eligible outdoor gear with verified reviews, star ratings, and prices.</li>
    <li><strong><code>optimize_budget_cart</code></strong>: Reconciles cart items against user-defined budget ceilings, calculating bundle discounts (-$12.50) and estimated tax.</li>
    <li><strong><code>confirm_order_execution</code></strong>: Enforces human-in-the-loop authorization tokens, generating secured one-touch approval cards before checkout.</li>
  </ul>

  <h2>3. Amazon Bedrock Autonomous Reasoning Engine</h2>
  <div class="grid-2">
    <div class="card">
      <strong>Autonomous Goal Decomposition</strong>
      <p style="margin-top:4px; font-size:12px;">When presented with complex goals like <em>"Plan a 3-day camping trip to Olympic National Park under $300 and buy needed gear"</em>, Bedrock deconstructs high-level requirements into parallel tool actions without human micro-management.</p>
    </div>
    <div class="card">
      <strong>Deterministic Safety Guardrails</strong>
      <p style="margin-top:4px; font-size:12px;">Financial and commerce commitments cannot execute autonomously without explicit human-in-the-loop confirmation. The agent constructs staged carts and renders a high-visibility approval card.</p>
    </div>
  </div>

  <h2>4. Production Deployment & Verification</h2>
  <ul>
    <li><strong>Production Live URL</strong>: <a href="https://omniflow-alexa-mcp.vercel.app/">https://omniflow-alexa-mcp.vercel.app/</a></li>
    <li><strong>MCP Protocol Discovery Endpoint</strong>: <code>https://omniflow-alexa-mcp.vercel.app/mcp/info</code></li>
    <li><strong>Code Repository</strong>: <a href="https://github.com/akshatanand-cell/omniflow-alexa-mcp">https://github.com/akshatanand-cell/omniflow-alexa-mcp</a></li>
    <li><strong>Demo Video (YouTube)</strong>: <a href="https://youtu.be/frLnS64f22E">https://youtu.be/frLnS64f22E</a></li>
  </ul>

  <div class="footer">
    <span>Author: Akshat Anand (akshatanand-cell)</span>
    <span>OmniFlow • Build, Ship, Shape: Amazon Developer Hackathon 2026</span>
    <span>Page 1 of 1</span>
  </div>

</body>
</html>
"""

async def generate_pdf():
    print("📄 Rendering Executive Whitepaper PDF with Playwright Chromium...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_content(HTML_CONTENT, wait_until="networkidle")
        await page.pdf(
            path=OUTPUT_PDF,
            format="A4",
            print_background=True,
            margin={"top": "15mm", "bottom": "15mm", "left": "15mm", "right": "15mm"}
        )
        await browser.close()
    print(f"✅ Executive Whitepaper PDF successfully generated at: {OUTPUT_PDF}")

if __name__ == "__main__":
    asyncio.run(generate_pdf())
