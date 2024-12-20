from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Configuration
BACKEND_URL = "https://chat-bot-api.bcpgroupe.com/chat/assistant-crc"
WHATSAPP_API_URL = "https://graph.facebook.com/v15.0/510480972147854/messages"
ACCESS_TOKEN = "EAAqDp1XkITcBO0TJJoGYUVXL8MjUcNU7Xw9yIonJp8F1ISSrwtItoLLyqXOfyFGohsE0ZADO24Dpvo41dh0LC6YMdmr2ZCIZBhWJkEZClvc4GaXpZBBjGUZC8rqGDsCBBVRLrzz0NCMTZAq4qbhary7vg6AFB40o0DUzX739fW67xQZAtZAZBIPHCZBnWFjZAYczqj9cDT6e2ZC7XjqOcvzOtR9ZBKGkZBkHxoZD"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    # Extraire le message de l'utilisateur
    user_message = data['messages'][0]['text']['body']
    sender_id = data['messages'][0]['from']

    # Appeler le backend Spring Boot
    response = requests.post(
        BACKEND_URL,
        json={
            "content": user_message,
            "instructions": "",
            "conversationId": 127  # Adapter selon la logique
        },
        headers={"Content-Type": "application/json"}
    )
    backend_reply = response.json().get("reply", "Je n'ai pas compris.")

    # Répondre via WhatsApp
    whatsapp_response = {
        "messaging_product": "whatsapp",
        "to": sender_id,
        "text": {"body": backend_reply}
    }
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    requests.post(WHATSAPP_API_URL, json=whatsapp_response, headers=headers)

    return jsonify({"status": "Message sent"}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
