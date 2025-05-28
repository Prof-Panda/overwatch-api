from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json
    teammates = ", ".join(data["teammates"])

    prompt = (
        f"I am playing OverWatch 2. Please provide a suggestion for which character I should play "
        f"as based on what my teammates are using. Remember, each team should have 1 tank, 2 DPS, and 2 support. "
        f"Here are the 4 characters my teammates are using: {teammates}"
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    recommendation = response["choices"][0]["message"]["content"]
    return jsonify({"recommendation": recommendation})

if __name__ == "__main__":
    app.run(debug=True)
