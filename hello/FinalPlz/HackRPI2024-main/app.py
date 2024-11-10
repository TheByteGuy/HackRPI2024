from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic
import base64
from PIL import Image
import io
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def encode_image_to_base64(image):
    """Convert image to base64 string"""
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

def analyze_image(image, api_key):
    """Analyze image using Claude 3.5 Sonnet"""
    client = anthropic.Client(api_key=api_key)
    base64_image = encode_image_to_base64(image)

    prompt = """
    You are a friendly wildlife expert creating an AMAZING ANIMAL ADVENTURE report for children. 
    Please format your response EXACTLY as follows (including all emojis, borders, and spacing):

    =============================
    🌟 AMAZING ANIMAL ADVENTURE! 🌟               
    =============================

    👋 Meet the [animal name]!
    (Scientists call them "[scientific name]" - that's their fancy name! 😊)

    ~~~~~~~~~~~~~~

    🎨 AWESOME FACTS TIME! 🎨
    ✨ [First exciting fact written in simple, fun language]
    ✨ [Second exciting fact written in simple, fun language]

    ~~~~~~~~~~~~~~

    📊 FRIENDLINESS SCALE 📊
    ╔══════════════════════════╗
    ║ 💚💚💚 Super Friendly!      ║
    ║ 💚💚   Friendly but Careful ║
    ║ 💚     Watch from Distance  ║
    ╚══════════════════════════╝

    🎯 THIS ANIMAL'S RATING:
    Friendliness: [Use exactly one: 💚💚💚, 💚💚, or 💚]
    How sure are we? [Use exactly one: 🌟🌟🌟, 🌟🌟, or 🌟]
    That means: [Simple explanation of the rating for kids]

    🤝 HOW TO BE FRIENDS:
    [2-3 lines of simple advice on how to interact with this animal]

    ✨ SPECIAL NOTE:
    [Important behavior or safety information written in a fun, non-scary way]

    ~~~~~~~~~~~~~~

    🦸 BE A SAFETY SUPERHERO! 🦸
    [3-4 lines of safety tips written in a positive, encouraging way]

    ~~~~~~~~~~~~~~

    🔍 DETECTIVE'S NOTEBOOK 🔍
    [Assessment if this is a wild animal or pet, followed by 3-4 bullet points of clues]
    - [Clue 1]
    - [Clue 2]
    - [Clue 3]
    - [Optional Clue 4]

    ~~~~~~~~~~~~~~

    🌟 FUN LEARNING CHECK! 🌟
    Can you remember...
    1. What's the special scientific name for this animal?
    2. [Question about a fact mentioned earlier]
    3. [Question about behavior or safety]

    🎨 CREATIVE CORNER 🎨
    Why not try:
    - [Creative activity suggestion 1]
    - [Creative activity suggestion 2]
    - Sharing these cool facts with your friends!

    ==============================
    🌈 Thanks for being an AWESOME Animal Explorer! 🌈
    ============================

    Remember to maintain child-friendly language throughout and keep everything positive and engaging!
    """
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {"type": "base64", "media_type": "image/jpeg", "data": base64_image}
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ],
    )
    response = message.content[0].text

    return response
    # Parsing response for structured JSON output
    try:
        parsed_response = {
            "common_name": response.split("Common name:")[1].split("\n")[0].strip(),
            "species_name": response.split("Species name:")[1].split("\n")[0].strip(),
            "fun_fact": response.split("Fun fact:")[1].split("\n")[0].strip(),
            "health_risks": response.split("Health risks:")[1].split("Stray assessment:")[0].strip(),
            "stray_assessment": response.split("Stray assessment:")[1].strip(),
        }
    except IndexError:
        return {"error": "Failed to parse the response format properly."}
    print('Parsed', parsed_response)


@app.route('/classify', methods=['POST'])
def classify():
    if 'photo' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files['photo']
    image = Image.open(file.stream)

    result = analyze_image(image, api_key)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
