import base64
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

def generate(text, instructions_file='novels/raon_instructions.txt'):
    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY"),
    )

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=text),
            ],
        )
    ]

    # Read instructions from file
    instructions_path = os.path.join(os.path.dirname(__file__), instructions_file)
    with open(instructions_path, 'r', encoding='utf-8') as f:
        instructions = f.read()

    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text=instructions),
        ],
    )

    result = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        result += chunk.text
    
    return result

if __name__ == "__main__":
    print(generate("Sample text"))
