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
    f"You are an Overwatch 2 coach helping a player choose the best hero to complete their team. "
    f"Each Overwatch team has 1 tank, 2 DPS, and 2 supports. "
    f"The player has 4 teammates already locked in: {teammates}. "
    f"Based on common team synergies, meta picks, role balance, and hero counters, recommend the best 5th hero to play. "

    f"Return your answer in the following format:\n\n"
    f"- **Recommended Pick**: <Hero Name>\n"
    f"- **Reason**: <1–2 sentence explanation>\n"
    f"- **Runner-Up**: <Hero Name>\n"
    f"- **Avoid**: <List of 2–3 heroes that would not work well with the team>\n"
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
