from flask import Flask, render_template, request
from model import predict_cost
import webbrowser

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    appliance = request.form["appliance"]
    power = int(request.form["power"])
    duration = int(request.form["duration"])
    time_of_use = int(request.form["time"])

    cost = predict_cost(power, duration, time_of_use)

    # Tariff detection
    if 6 <= time_of_use <= 10 or 18 <= time_of_use <= 22:
        tariff = "Peak"
        peak_cost = cost
        offpeak_cost = round(cost * 0.5, 2)

    elif 10 < time_of_use < 18:
        tariff = "Normal"
        peak_cost = round(cost * 1.2, 2)
        offpeak_cost = round(cost * 0.6, 2)

    else:
        tariff = "Off-Peak"
        peak_cost = round(cost * 1.5, 2)
        offpeak_cost = cost

    savings = round(peak_cost - offpeak_cost, 2)

    if tariff == "Peak":
        suggestion = "⚡ Better to use during OFF-PEAK hours (10PM – 6AM)"
    else:
        suggestion = "✅ Good time to use appliance (Low tariff period)"

    # WhatsApp message
    message = f"""
Smart Power Optimizer

Appliance: {appliance}
Estimated Cost: ₹{cost}
Tariff: {tariff}
Savings: ₹{savings}

Suggestion:
{suggestion}
"""

    # Send message through WhatsApp link
    phone = "918438421765"   # replace with your number

    url = f"https://wa.me/{phone}?text={message}"
    webbrowser.open(url)

    return render_template(
        "index.html",
        appliance=appliance,
        cost=cost,
        tariff=tariff,
        suggestion=suggestion,
        savings=savings
    )


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
