from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    intent_name = req["queryResult"]["intent"]["displayName"]

    if intent_name == "OrderTrackingIntent":
        order_number = req["queryResult"]["parameters"]["order_number"]
        fulfillment_text = f"Tracking information for order {order_number}: In transit"
    elif intent_name == "ReturnPolicyIntent":
        fulfillment_text = "Our return policy allows for returns within 30 days of purchase."
    else:
        fulfillment_text = "Sorry, I'm not sure how to help with that."

    return jsonify({'fulfillmentText': fulfillment_text})

if __name__ == '__main__':
    app.run()

