import os
import sys
import subprocess
import asyncio
import textwrap
from PIL import Image, ImageDraw, ImageFont

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = os.path.join(os.path.dirname(__file__), "..")
CAPTURES_DIR = os.path.join(ROOT_DIR, "live_captures")
OUTPUT_DIR = os.path.join(ROOT_DIR, "video_assets")
os.makedirs(OUTPUT_DIR, exist_ok=True)

WIDTH, HEIGHT = 1920, 1080
NEURAL_VOICE = "en-US-AriaNeural"

# Scenes combining real live app screenshots with bold, wrapped captions and narration
SCENES = [
    {
        "image": "live_01_home.png",
        "narration": "Welcome to OmniFlow! Built for the Amazon Developer Hackathon 2026, OmniFlow transforms Alexa Plus into an autonomous life and commerce copilot using the Model Context Protocol and Amazon Bedrock.",
        "caption": "OmniFlow: Autonomous Alexa+ Copilot powered by MCP (2025-11-25) & Amazon Bedrock."
    },
    {
        "image": "live_02_results.png",
        "narration": "When a user asks to plan a three-day camping trip to Olympic National Park under 300 dollars, OmniFlow autonomously coordinates multiple MCP tools: planning the itinerary, checking weather, and finding Prime camping essentials.",
        "caption": "Autonomous Planning: Deconstructs goal into daily itinerary & queries Amazon Prime catalog."
    },
    {
        "image": "live_03_budget_cart.png",
        "narration": "Notice the multi-modal cards! The agent calculates bundle discounts, estimates tax, and verifies that the total remains strictly within the 300-dollar budget ceiling before staging the cart.",
        "caption": "Multi-Modal Intelligence: Dynamic budget meter, bundle discounts (-$12.50), & cart optimization."
    },
    {
        "image": "live_04_mcp_inspector.png",
        "narration": "Under the hood, developers can inspect live JSON-RPC 2.0 messages streaming over Streamable HTTP, adhering to the latest MCP specification version 2025-11-25.",
        "caption": "Live MCP Inspector: Inspecting raw JSON-RPC 2.0 messages streaming over Streamable HTTP."
    },
    {
        "image": "live_05_order_confirmed.png",
        "narration": "Finally, OmniFlow enforces a strict human-in-the-loop safety guardrail. Orders require explicit one-touch confirmation before checkout is authorized. Try it live at omniflow-alexa-mcp.vercel.app!",
        "caption": "Human-in-the-Loop Safety: One-touch order confirmation guardrail. Live on Vercel!"
    }
]

def get_bold_font(size):
    for fn in ["segoeuib.ttf", "arialbd.ttf", "calibrib.ttf", "impact.ttf"]:
        try:
            return ImageFont.truetype(fn, size)
        except Exception:
            continue
    return ImageFont.load_default()

def overlay_captions(input_img_path, caption_text, output_img_path):
    # Open real screenshot from Vercel
    base_img = Image.open(input_img_path).convert("RGBA")
    base_img = base_img.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)

    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Word wrap caption so it NEVER goes off screen (max 50 chars per line)
    lines = textwrap.wrap(caption_text, width=52)

    font_caption = get_bold_font(32)
    font_badge = get_bold_font(16)

    # Calculate height needed for caption box
    line_height = 42
    box_height = 50 + len(lines) * line_height
    box_y1 = HEIGHT - box_height - 35
    box_y2 = HEIGHT - 35

    # Draw modern rounded translucent backdrop for subtitles
    box_rect = [(80, box_y1), (WIDTH - 80, box_y2)]
    draw.rounded_rectangle(box_rect, radius=18, fill=(3, 7, 18, 235), outline=(0, 168, 225, 240), width=3)

    # Caption Tag Pill
    draw.rounded_rectangle([(115, box_y1 + 14), (275, box_y1 + 42)], radius=6, fill=(0, 168, 225), outline=(255, 255, 255), width=1)
    draw.text((130, box_y1 + 18), "LIVE DEMO", fill=(255, 255, 255), font=font_badge)

    # Deployed URL indicator on top right of caption box
    draw.text((WIDTH - 440, box_y1 + 18), "omniflow-alexa-mcp.vercel.app", fill=(56, 189, 248), font=font_badge)

    # Render bold wrapped lines with slight drop shadow
    start_y = box_y1 + 52
    for i, line in enumerate(lines):
        y = start_y + i * line_height
        # Shadow
        draw.text((117, y + 2), line, fill=(0, 0, 0, 220), font=font_caption)
        # Main text
        draw.text((115, y), line, fill=(255, 255, 255), font=font_caption)

    # Composite overlay on top of screenshot
    final_img = Image.alpha_composite(base_img, overlay).convert("RGB")
    final_img.save(output_img_path, quality=95)
    return output_img_path

async def synthesize_speech(text, out_path):
    import edge_tts
    comm = edge_tts.Communicate(text, NEURAL_VOICE, rate="+4%")
    await comm.save(out_path)

def main():
    print("🎬 Assembling true live demo video from Vercel screenshots with bold captions & Neural AI Voice...")
    clips = []

    for i, scene in enumerate(SCENES):
        print(f"  [Scene {i+1}/{len(SCENES)}] Processing live capture: {scene['image']}...")
        raw_capture = os.path.join(CAPTURES_DIR, scene["image"])
        framed_img = os.path.join(OUTPUT_DIR, f"live_framed_{i}.png")
        audio_path = os.path.join(OUTPUT_DIR, f"live_audio_{i}.mp3")

        # 1. Overlay bold, word-wrapped captions that never spill off screen
        overlay_captions(raw_capture, scene["caption"], framed_img)

        # 2. Synthesize studio Neural AI speech
        asyncio.run(synthesize_speech(scene["narration"], audio_path))

        # 3. Measure duration with ffprobe
        probe_cmd = f'ffprobe -i "{audio_path}" -show_entries format=duration -v quiet -of csv="p=0"'
        duration_str = subprocess.check_output(probe_cmd, shell=True).decode().strip()
        duration = float(duration_str) + 1.2 # smooth transition buffer

        # 4. Generate video clip for scene
        clip_path = os.path.join(OUTPUT_DIR, f"live_clip_{i}.mp4")
        cmd = f'ffmpeg -y -loop 1 -i "{framed_img}" -i "{audio_path}" -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -t {duration} "{clip_path}"'
        subprocess.check_call(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        clips.append(clip_path)

    # 5. Merge all clips into final demo_video.mp4
    concat_txt = os.path.join(OUTPUT_DIR, "live_clips.txt")
    with open(concat_txt, "w") as f:
        for c in clips:
            f.write(f"file '{c.replace(os.sep, '/')}'\n")

    final_video = os.path.join(ROOT_DIR, "demo_video.mp4")
    print(f"🎥 Merging scenes into final high-def demo: {final_video}...")
    merge_cmd = f'ffmpeg -y -f concat -safe 0 -i "{concat_txt}" -c copy "{final_video}"'
    subprocess.check_call(merge_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print("✅ LIVE DEMO VIDEO SUCCESSFULLY GENERATED!")
    print(f"📁 Video Location: {os.path.abspath(final_video)}")

if __name__ == "__main__":
    main()
