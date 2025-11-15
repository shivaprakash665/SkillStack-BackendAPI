# test_simple.py
import requests
import json

def test_simple():
    test_notes = """
    Machine learning is a subset of artificial intelligence. Important concepts include 
    supervised learning where models learn from labeled data, and unsupervised learning 
    where patterns are found in unlabeled data. Key algorithms include decision trees, 
    neural networks, and support vector machines. The main goal is to enable computers 
    to learn automatically without human intervention.
    """
    
    payload = {
        "notes": test_notes,
        "session_id": 1
    }
    
    try:
        response = requests.post(
            'http://localhost:5000/api/learning/ai/summarize',
            json=payload
        )
        
        print("Status:", response.status_code)
        result = response.json()
        print("Summary:", result.get('summary'))
        print("Model:", result.get('model'))
        
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test_simple()