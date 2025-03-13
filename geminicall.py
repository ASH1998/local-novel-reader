import base64
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

def generate(text):
    client = genai.Client(
        api_key=os.getenv('GEMINI_API_KEY'),
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
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""Translate Korean text into high-quality English in markdown format while preserving the original tone, context, and meaning as accurately as possible. Ensure that cultural nuances, idiomatic expressions, and emotions conveyed in the source text are properly adapted for English-speaking audiences.

# Additional Details

- Maintain the original narrative style, whether formal, literary, casual, or conversational.
- Ensure that character dialogues feel natural in English and reflect the personalities, tone, and emotions conveyed in the Korean text.
- For cultural references or idiomatic expressions that do not have direct English equivalents, provide a localized adaptation or include a brief clarification in brackets.
- Break down lengthy sentences into clear and natural English sentences where needed, without losing meaning or complexity.
- Aim for fluency and readability in English, while staying true to the original content.

# Steps

1. **Understand the Context**: Read and interpret the Korean source text fully before translating. Pay attention to implied meanings, emotions, and tone.
2. **Translate**: Use clear English phrasing that accurately represents the source content. Avoid overly literal translations unless absolutely necessary.
3. **Cultural Adaptation**: Adjust references, idioms, or wordplay for better understanding by English-speaking audiences. Include notes or brackets where applicable.
4. **Refine for Flow**: Review the English text to ensure fluency, coherence, grammar, and overall readability.
5. **Preserve Original Paragraphing**: Divide the translated text with the same breaks or structure used in the Korean source material unless readability dictates otherwise.

# Output Format

- Structure: Provide the English translation as a natural and readable narrative. Use paragraphs to match the flow of the source text.
- Clarity: Use proper punctuation and grammar for polished output.

(Include placeholders for longer or more complex chapters as necessary, always matching given tone and style.)

# Notes

- If specific chapters or entire novels are requested for translation, provide the output in sections (e.g., chapter-by-chapter). Ensure logical breaks for readability.
- If faced with ambiguous text, provide your best interpretation and explain unclear phrases in parentheses or footnotes.
- Always prioritize readability and narrative flow in English over strict literal translation.
                                 

# Here are some characters and some descriptions of them:
Raon: The main character of the story
Glenn: Raon's grandfather
Zieghart: The clan of Raon
Some other important characters from Zeighart family are: Rimmer, Wrath, Sylvia, Roenn, Martha, Light wind divison, Light Wind Palace, Runann, Burren, Karoon, Aries, Balder, Raden, Merlin
Some names of power levels : novice, expert, master, grandmaster, transcendent, divine. Each level has beginner, intermediate, advanced, and peak stages.

Raon Zieghart (main character)
Zieghart Ancestor (maternal ancestor)
Glenn Zieghart (maternal grandfather)
Rector (paternal grandfather)
Edgar (father)
Sylvia Zieghart (mother)
Sia Zieghart (sister)
Karoon Zieghart (uncle)
Gelmia Zieghart (cousin)
Burren Zieghart (cousin)
Balder Zieghart (uncle)
Garon Zieghart (cousin)
Raden Zieghart (cousin)
Aris Zieghart (aunt)
Sif Zieghart ✝ (cousin)
Deiner Zieghart ✝ (uncle)
Martha Zeighart (adoptive cousin)    

Instructor
Rimmer
                                 
Friends
Wrath
Merlin
                                 
Master
Rimmer
                                 
Subordinates
Judiel
Dorian Sephia
Harian Zieghart
Mark Goetten
Wendy Arianne
Mustan
Light Wind Palace
                                 
Allies
Hoppen(Suphren Kingdom)
                                 
Enemies
Derus Robert
Fallen
The Heavenly Demon
Holy Sword Alliance(Formerly)
White Blood Religion leader
Tenth Apostle
Roman Reycal
South-North Union
Angels
Dragons
Pride

Make sure to use these names                                 
                                 
"""),
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
    print(generate())
