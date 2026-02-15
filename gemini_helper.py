import google.generativeai as genai

genai.configure(api_key="GOOGLE_API_KEY")

prompt = "Write a short poem about pizza."

try:
    response = genai.generate_text(
        model="gemini-1",
        prompt=prompt
    )
    print(response.text)
except Exception as e:
    print("Error:", e)
