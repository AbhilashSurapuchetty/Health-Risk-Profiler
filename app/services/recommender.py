# app/services/recommender.py
import os
from groq import Groq

def generate_recommendations(factors, risk_level):
    """
    Generate AI-based recommendations using Groq API,
    fallback to static if API call fails.
    """
    api_key = os.getenv("GROQ_API_KEY")
    recs = []

    try:
        client = Groq(api_key=api_key)

        prompt = (
            "You are a health and wellness assistant. "
            "The user has the following lifestyle-related health risk profile:\n\n"
            f"Risk level: {risk_level}\n"
            f"Factors: {', '.join(factors)}\n\n"
            "Your task:\n"
            "1. Suggest 3–5 clear, actionable lifestyle recommendations.\n"
            "2. Avoid any diagnostic or medical claims.\n"
            "3. Keep the language simple and encouraging.\n"
            "4. Output each recommendation as a short bullet point."
        )


        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful health assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=150
        )

        ai_reply = response.choices[0].message.content.strip()
        recs = [line.strip("-• ") for line in ai_reply.split("\n") if line.strip()]

    except Exception as e:
        print(f"[Fallback triggered] {e}")
        if "smoking" in factors:
            recs.append("Quit smoking gradually with support.")
        if "poor diet" in factors:
            recs.append("Reduce sugar and eat more vegetables.")
        if "low exercise" in factors:
            recs.append("Start with 30 minutes of walking daily.")
        if not recs:
            recs.append("Maintain a balanced diet and active lifestyle.")

    return recs
