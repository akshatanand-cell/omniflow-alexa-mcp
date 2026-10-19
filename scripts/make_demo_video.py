import os
import sys
import subprocess
import asyncio
from PIL import Image, ImageDraw, ImageFont

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "video_assets")
os.makedirs(OUTPUT_DIR, exist_ok=True)

WIDTH, HEIGHT = 1920, 1080

# Professional Neural AI Voice (Aria is crisp, fluent, and professional)
NEURAL_VOICE = "en-US-AriaNeural"

SLIDES = [
    {
        "tag": "OVERVIEW",
        "title": "OmniFlow: Agentic Alexa+ Life & Commerce Copilot",
        "subtitle": "Model Context Protocol (v2025-11-25) & Amazon Bedrock",
        "bullets": [
            "Traditional voice assistants are reactive. OmniFlow introduces autonomous agentic execution.",
            "Full compliance with Model Context Protocol (MCP) Specification version 2025-11-25.",
            "Integrated with Amazon Bedrock using Claude 3.5 Sonnet for multi-step reasoning.",
            "Designed for multi-modal screen devices: Echo Show, Fire TV, and modern Web clients."
        ],
        "speech": "Hi everyone! Welcome to OmniFlow, an autonomous life and commerce copilot built for the Amazon Developer Hackathon 2026. While traditional voice assistants are reactive, OmniFlow leverages the Model Context Protocol and Amazon Bedrock to autonomously plan, compare, and execute complex multi-step goals.",
        "color": (0, 168, 225) # Alexa Cyan
    },
    {
        "tag": "ARCHITECTURE",
        "title": "Decoupled Architecture & Streamable HTTP",
        "subtitle": "4 Production-Ready MCP Tools over Streamable HTTP Transport",
        "bullets": [
            "plan_itinerary: Formulates multi-day schedules, activities, and weather forecasts.",
            "search_amazon_products: Queries Prime catalog with ratings, live prices, and badges.",
            "optimize_budget_cart: Analyzes budget ceilings and applies bundle discounts.",
            "confirm_order_execution: Enforces human-in-the-loop one-touch authorization."
        ],
        "speech": "OmniFlow implements the official 2025-11-25 MCP specification over modern Streamable HTTP transports. It registers four specialized tools: planning itineraries, searching Amazon for Prime gear, optimizing bundle budgets, and securing one-click checkout.",
        "color": (16, 185, 129) # Emerald
    },
    {
        "tag": "AUTONOMOUS EXECUTION",
        "title": "Autonomous Multi-Step Execution in Action",
        "subtitle": "Goal: 3-Day Olympic National Park Camping Trip Under $300",
        "bullets": [
            "Step 1: Itinerary Formulation - 3-day schedule with 6 outdoor activities ($60 estimated).",
            "Step 2: Amazon Product Discovery - Coleman tent, Vont lanterns, and camp stoves.",
            "Step 3: Cart & Budget Optimization - Bundle discount applied (-$12.50), final total $163.97.",
            "Step 4: Budget Enforcement - Total falls safely within the user's $300 limit."
        ],
        "speech": "When a user gives a high-level goal, such as planning a camping trip under 300 dollars, OmniFlow deconstructs the request, queries tools in sequence, finds top-rated Prime camping essentials, and ensures the total remains strictly within budget.",
        "color": (245, 158, 11) # Amber
    },
    {
        "tag": "MULTI-MODAL UX",
        "title": "Interactive Multi-Modal Cards & UI",
        "subtitle": "Echo Show, Fire TV, and Web Simulator Experience",
        "bullets": [
            "Dynamic Itinerary Timeline: Interactive daily tabs and localized weather forecasts.",
            "Prime Product Carousel: Horizontal media card swiper with reviews and badges.",
            "Real-Time Budget Meter: Visual progress tracking against the user's budget ceiling.",
            "Integrated Speech: Bi-directional speech recognition and ambient Alexa voice synthesis."
        ],
        "speech": "Rather than returning plain audio answers, OmniFlow renders interactive multi-modal cards. Users can swipe through Prime product carousels, view interactive itinerary timelines, and track budget utilization in real time.",
        "color": (139, 92, 246) # Purple
    },
    {
        "tag": "DEVELOPER EXPERIENCE & SAFETY",
        "title": "Live MCP Protocol Inspector & Human Guardrails",
        "subtitle": "Developer Observability + Production Safety Standard",
        "bullets": [
            "Real-time JSON-RPC 2.0 inspector streaming live over /mcp/stream.",
            "Strict Human-in-the-Loop guardrail prevents accidental or hallucinated purchases.",
            "Complete Product Feedback and Friction Log submitted for Amazon DevRel (+10% Bonus).",
            "Production deployment live at omniflow-alexa-mcp.vercel.app."
        ],
        "speech": "OmniFlow also features a live Protocol Inspector for developers to examine streamable JSON-RPC messages, and enforces a human-in-the-loop guardrail before any transaction is executed. Our project is fully open source on GitHub and deployed live on Vercel. Thank you!",
        "color": (236, 72, 153) # Pink
    }
]

def get_font(size, bold=False):
    font_names = ["segoeui.ttf", "arial.ttf", "calibri.ttf"]
    if bold:
        font_names = ["segoeuib.ttf", "arialbd.ttf", "calibrib.ttf"]
    for fn in font_names:
        try:
            return ImageFont.truetype(fn, size)
        except Exception:
            continue
    return ImageFont.load_default()

def render_slide(slide, index):
    img = Image.new("RGB", (WIDTH, HEIGHT), (2, 6, 23)) # Slate-950
    draw = ImageDraw.Draw(img)

    # Gradient backdrop simulation
    for y in range(HEIGHT):
        alpha = y / HEIGHT
        r = int(2 + alpha * 10)
        g = int(6 + alpha * 14)
        b = int(23 + alpha * 20)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    # Top Header Card
    draw.rounded_rectangle([(100, 60), (WIDTH - 100, 140)], radius=16, fill=(30, 41, 59, 200), outline=(51, 65, 85), width=2)
    draw.ellipse([(130, 85), (160, 115)], fill=slide["color"])
    
    font_header_brand = get_font(26, bold=True)
    draw.text((180, 85), "OmniFlow", fill=(56, 189, 248), font=font_header_brand)
    
    font_header_sub = get_font(18)
    draw.text((320, 92), "|  Build, Ship, Shape: Amazon Developer Hackathon 2026", fill=(148, 163, 184), font=font_header_sub)

    # Track badge
    draw.rounded_rectangle([(WIDTH - 440, 80), (WIDTH - 130, 120)], radius=8, fill=(3, 105, 161), outline=(2, 132, 199), width=1)
    font_badge = get_font(16, bold=True)
    draw.text((WIDTH - 420, 90), "Alexa+ Track • MCP 2025-11-25", fill=(224, 242, 254), font=font_badge)

    # Main Center Card
    draw.rounded_rectangle([(100, 170), (WIDTH - 100, 860)], radius=24, fill=(15, 23, 42), outline=(30, 41, 59), width=2)

    # Tag Pill
    draw.rounded_rectangle([(160, 210), (360, 248)], radius=6, fill=slide["color"], outline=slide["color"], width=1)
    font_tag = get_font(14, bold=True)
    draw.text((180, 222), slide["tag"], fill=(255, 255, 255), font=font_tag)

    # Title & Subtitle
    font_title = get_font(46, bold=True)
    draw.text((160, 265), slide["title"], fill=(255, 255, 255), font=font_title)

    font_sub = get_font(22)
    draw.text((160, 325), slide["subtitle"], fill=(148, 163, 184), font=font_sub)

    # Divider line
    draw.line([(160, 370), (WIDTH - 160, 370)], fill=(51, 65, 85), width=2)

    # Bullets
    font_bullet = get_font(24)
    start_y = 420
    for i, b in enumerate(slide["bullets"]):
        y = start_y + i * 90
        draw.ellipse([(165, y + 6), (185, y + 26)], fill=slide["color"])
        draw.text((215, y), b, fill=(226, 232, 240), font=font_bullet)

    # Bottom Audio Indicator Box
    draw.rounded_rectangle([(100, 890), (WIDTH - 100, 1010)], radius=18, fill=(2, 6, 23), outline=(2, 132, 199), width=2)
    font_cap_label = get_font(15, bold=True)
    draw.text((140, 910), "🎙️ NEURAL AI VOICE NARRATION (Aria Neural)", fill=(56, 189, 248), font=font_cap_label)

    font_cap = get_font(21)
    draw.text((140, 945), slide["speech"], fill=(248, 250, 252), font=font_cap)

    png_path = os.path.join(OUTPUT_DIR, f"slide_{index}.png")
    img.save(png_path)
    return png_path

async def generate_neural_speech(text, output_path):
    import edge_tts
    communicate = edge_tts.Communicate(text, NEURAL_VOICE, rate="+5%")
    await communicate.save(output_path)

def main():
    print("🎬 Generating presentation with Neural AI Voice Narration...")
    clips = []

    for i, slide in enumerate(SLIDES):
        print(f"  [Slide {i+1}/5] Rendering visual frame and synthesizing Neural Voice ({slide['tag']})...")
        img_path = render_slide(slide, i)
        audio_path = os.path.join(OUTPUT_DIR, f"audio_neural_{i}.mp3")

        # Generate Neural Audio with edge-tts
        asyncio.run(generate_neural_speech(slide["speech"], audio_path))

        # Get audio duration using ffprobe
        probe_cmd = f'ffprobe -i "{audio_path}" -show_entries format=duration -v quiet -of csv="p=0"'
        duration_str = subprocess.check_output(probe_cmd, shell=True).decode().strip()
        duration = float(duration_str) + 1.2 # 1.2s smooth slide transition buffer
        
        # Create individual video clip
        clip_path = os.path.join(OUTPUT_DIR, f"clip_{i}.mp4")
        create_clip_cmd = f'ffmpeg -y -loop 1 -i "{img_path}" -i "{audio_path}" -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -t {duration} "{clip_path}"'
        subprocess.check_call(create_clip_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        clips.append(clip_path)

    # Concat all clips into final demo_video.mp4
    concat_list_file = os.path.join(OUTPUT_DIR, "clips.txt")
    with open(concat_list_file, "w") as f:
        for c in clips:
            f.write(f"file '{c.replace(os.sep, '/')}'\n")

    final_video_path = os.path.join(os.path.dirname(__file__), "..", "demo_video.mp4")
    print(f"🎥 Merging clips into final high-def demo video with Neural AI Voice...")
    concat_cmd = f'ffmpeg -y -f concat -safe 0 -i "{concat_list_file}" -c copy "{final_video_path}"'
    subprocess.check_call(concat_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print("✅ NEURAL AI VOICE DEMO VIDEO SUCCESSFULLY GENERATED!")
    print(f"📁 Video Location: {os.path.abspath(final_video_path)}")

if __name__ == "__main__":
    main()
