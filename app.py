from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

# Initialize OpenAI client using API key from environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json
    teammates = ", ".join(data["teammates"])

    # Updated prompt with strict role mapping and role balance logic
    prompt = (
        "You are an expert Overwatch 2 coach. Every team must include exactly 1 tank, 2 damage (DPS), and 2 support heroes — no exceptions. "
        "You will be given 4 teammates' heroes and must recommend the best 5th hero to complete the team. "
        "Use the hero role list below to ensure correct role balance:\n\n"
        "Tanks: D.Va, Doomfist, Junker Queen, Mauga, Orisa, Ramattra, Reinhardt, Roadhog, Sigma, Winston, Wrecking Ball, Zarya\n"
        "Damage: Ashe, Bastion, Cassidy, Echo, Genji, Hanzo, Junkrat, Mei, Pharah, Reaper, Sojourn, Soldier: 76, Sombra, Symmetra, Torbjorn, Tracer, Venture, Widowmaker\n"
        "Support: Ana, Baptiste, Brigitte, Illari, Kiriko, Lifeweaver, Lucio, Mercy, Moira, Zenyatta\n\n"
        f"The current team already includes: {teammates}. "
        "Determine which role is missing. Recommend a hero from that role that complements the team in terms of strategy, synergy, and meta. "
        "Never recommend a second tank or a third support or third DPS.\n\n"
        "Return your answer using this format:\n"
        "- **Recommended Pick**: <Hero Name> (<Hero Role>)\n"
        "- **Reason**: <Short explanation>\n"
        "- **Runner-Up**: <Hero Name> (<Hero Role>)\n"
        "- **Avoid**: <2–3 heroes that would disrupt team balance or synergy>\n"
    )

    # Make the call to OpenAI's Chat API
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    recommendation = response.choices[0].message.content
    return jsonify({"recommendation": recommendation})

if __name__ == "__main__":
    app.run(debug=True)
