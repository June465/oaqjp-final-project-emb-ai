import requests
import json

def emotion_detector(text_to_analyze):
    api_url = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    api_headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    request_payload = {
        "raw_document": {
            "text": text_to_analyze
        }
    }

    try:
        response = requests.post(api_url, headers=api_headers, json=request_payload)
        response.raise_for_status()
        response_data = response.json()
        
        emotion_predictions = response_data.get("emotionPredictions", [{}])[0]
        detected_emotions = emotion_predictions.get("emotion", {})
        
        emotion_scores = {
            'anger': detected_emotions.get('anger', 0),
            'disgust': detected_emotions.get('disgust', 0),
            'fear': detected_emotions.get('fear', 0),
            'joy': detected_emotions.get('joy', 0),
            'sadness': detected_emotions.get('sadness', 0),
        }

        dominant_emotion = max(emotion_scores, key=emotion_scores.get)
        emotion_scores['dominant_emotion'] = dominant_emotion

        return emotion_scores
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }
