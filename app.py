from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json
    teammates = ", ".join(data["teammates"])

   prompt = (
    f"You are an expert Overwatch 2 coach. Each team must have exactly 1 tank, 2 damage (DPS), and 2 support heroes — no exceptions. "
    f"The player already has 4 teammates using these heroes: {teammates}. "
    f"Your job is to recommend the best 5th hero **to fill the missing role**, based on the current team composition, role balance, and hero synergies. "
    f"First, identify which role is missing. Then suggest a hero from that role who best complements the team. "

    f"Return your answer in the following format:\n"
    f"- **Recommended Pick**: <Hero Name> (<Hero Role>)\n"
    f"- **Reason**: <Short synergy or strategy explanation>\n"
    f"- **Runner-Up**: <Hero Name> (<Hero Role>)\n"
    f"- **Avoid**: <2–3 heroes that would disrupt team balance or synergy>\n\n"

    f"⚠️ Important: Do not recommend a hero if their role would result in more than 1 tank, more than 2 damage, or more than 2 supports."
)


    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    recommendation = response.choices[0].message.content
    return jsonify({"recommendation": recommendation})

if __name__ == "__main__":
    app.run(debug=True)
