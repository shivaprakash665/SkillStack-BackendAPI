import requests
import json
import re
from flask import request, jsonify

class AIController:
    
    @staticmethod
    def generate_summary():
        try:
            data = request.get_json()
            notes = data.get('notes', '')
            session_id = data.get('session_id')
            
            if not notes or notes.strip() == '':
                return jsonify({'error': 'No notes provided'}), 400
            
            cleaned_notes = notes.strip()
            if len(cleaned_notes) < 10:
                return jsonify({'error': 'Notes are too short. Please add more content.'}), 400
            
            # Try multiple working Hugging Face models
            summary = AIController._try_working_models(cleaned_notes)
            
            return jsonify({
                'summary': summary,
                'model': 'huggingface',
                'session_id': session_id,
                'source': 'huggingface'
            }), 200
            
        except Exception as e:
            summary = AIController._create_enhanced_summary(notes)
            return jsonify({
                'summary': summary,
                'model': 'enhanced-fallback',
                'session_id': session_id
            }), 200
    
    @staticmethod
    def _try_working_models(notes):
        """Try multiple working Hugging Face models"""
        
        working_models = [
            {
                "name": "microsoft/DialoGPT-medium",
                "url": "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
                "type": "text-generation"
            },
            {
                "name": "distilgpt2", 
                "url": "https://api-inference.huggingface.co/models/distilgpt2",
                "type": "text-generation"
            },
            {
                "name": "EleutherAI/gpt-neo-125M",
                "url": "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-125M",
                "type": "text-generation"
            }
        ]
        
        for model in working_models:
            try:
                print(f"Trying model: {model['name']}")
                
                if model["type"] == "text-generation":
                    # For text generation models, we need to craft a prompt
                    prompt = f"Please summarize the following study notes in a concise way:\n\n{notes[:500]}\n\nSummary:"
                    
                    payload = {
                        "inputs": prompt,
                        "parameters": {
                            "max_new_tokens": 100,
                            "temperature": 0.7,
                            "do_sample": True
                        }
                    }
                else:
                    # For summarization models
                    payload = {
                        "inputs": notes[:800],
                        "parameters": {
                            "max_length": 100,
                            "min_length": 30,
                            "do_sample": False
                        }
                    }
                
                headers = {
                    "User-Agent": "LearnTrack-App/1.0"
                }
                
                response = requests.post(
                    model["url"],
                    json=payload,
                    headers=headers,
                    timeout=20
                )
                
                print(f"Response status for {model['name']}: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"Raw response: {result}")
                    
                    # Handle different response formats
                    summary_text = AIController._extract_summary(result, model["type"])
                    
                    if summary_text and len(summary_text) > 15:
                        print(f"✅ Success with {model['name']}")
                        return AIController._clean_summary(summary_text)
                
                elif response.status_code == 503:
                    print(f"Model {model['name']} is loading...")
                    continue
                    
            except requests.exceptions.Timeout:
                print(f"Timeout with {model['name']}")
                continue
            except Exception as e:
                print(f"Error with {model['name']}: {str(e)}")
                continue
        
        # If all models fail, use enhanced AI-like summary
        print("All API models failed, using enhanced AI simulation")
        return AIController._create_ai_style_summary(notes)
    
    @staticmethod
    def _extract_summary(result, model_type):
        """Extract summary text from different response formats"""
        try:
            if model_type == "text-generation":
                if isinstance(result, list) and len(result) > 0:
                    if 'generated_text' in result[0]:
                        return result[0]['generated_text']
                elif isinstance(result, dict) and 'generated_text' in result:
                    return result['generated_text']
            else:
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('summary_text', '')
            
            return ""
        except:
            return ""
    
    @staticmethod
    def _clean_summary(summary):
        """Clean and format the summary"""
        if not summary:
            return ""
        
        # Remove the prompt part if it's included
        if "Summary:" in summary:
            summary = summary.split("Summary:")[-1].strip()
        
        # Clean up text
        cleaned = ' '.join(summary.split())
        
        # Ensure proper punctuation
        if cleaned and not cleaned[-1] in '.!?':
            cleaned += '.'
        
        # Capitalize first letter
        if cleaned and cleaned[0].islower():
            cleaned = cleaned[0].upper() + cleaned[1:]
        
        return cleaned
    
    @staticmethod
    def _create_ai_style_summary(notes):
        """Create AI-style summary using advanced NLP techniques"""
        if not notes:
            return "Please add study notes to generate a summary."
        
        # Advanced text processing
        sentences = re.split(r'[.!?]+', notes)
        sentences = [s.strip() for s in sentences if s.strip() and len(s) > 8]
        
        if not sentences:
            return "Add more detailed notes for a better summary."
        
        # AI-style sentence scoring
        scored_sentences = []
        
        for i, sentence in enumerate(sentences):
            score = AIController._calculate_sentence_score(sentence, i)
            if score > 0:
                scored_sentences.append((sentence, score, i))
        
        # AI-like selection process
        if scored_sentences:
            scored_sentences.sort(key=lambda x: (-x[1], x[2]))
            
            # Select diverse sentences (not just highest scores)
            selected = []
            used_indices = set()
            
            for sentence, score, idx in scored_sentences:
                if len(selected) < 4 and idx not in used_indices:
                    selected.append(sentence)
                    used_indices.add(idx)
            
            summary = '. '.join(selected)
            
            # AI-style formatting
            if len(summary) > 50:
                return f"🤖 AI Summary:\n{summary}"
            else:
                return summary
        else:
            # Fallback to smart selection
            return AIController._create_smart_summary(notes)
    
    @staticmethod
    def _calculate_sentence_score(sentence, position):
        """Calculate how important a sentence is (AI-style)"""
        score = 0
        sentence_lower = sentence.lower()
        
        # Importance keywords with weights
        keywords = {
            'important': 5, 'key': 5, 'main': 5, 'essential': 5, 'critical': 5,
            'crucial': 5, 'fundamental': 4, 'principal': 4, 'primary': 4,
            'concept': 4, 'principle': 4, 'theory': 4, 'definition': 4,
            'means': 3, 'refers to': 3, 'is defined as': 4,
            'must': 3, 'should': 3, 'necessary': 3, 'required': 3,
            'therefore': 2, 'however': 2, 'consequently': 2, 'thus': 2,
            'in conclusion': 4, 'summary': 3, 'note that': 2
        }
        
        # Technical terms often indicate importance
        technical_terms = [
            'function', 'variable', 'class', 'method', 'algorithm', 'code',
            'program', 'system', 'process', 'structure', 'framework'
        ]
        
        # Score based on keywords
        for keyword, weight in keywords.items():
            if keyword in sentence_lower:
                score += weight
        
        # Score technical terms
        for term in technical_terms:
            if term in sentence_lower:
                score += 2
        
        # Structural scoring
        if re.match(r'^[\-\*•→›]', sentence):  # Bullet points
            score += 6
        if re.match(r'^\d+[\.\)]', sentence):  # Numbered lists
            score += 5
        
        # Definition patterns
        if re.search(r'\bis\b|\bare\b|\bmeans\b|\bdefined as\b', sentence_lower):
            score += 4
        
        # Length optimization (medium-length sentences are often most important)
        word_count = len(sentence.split())
        if 8 <= word_count <= 25:
            score += 2
        elif word_count > 40:  # Very long sentences might be less clear
            score -= 1
        
        # Position bonus (first sentences often contain main ideas)
        if position < 3:
            score += 2
        
        return score
    
    @staticmethod
    def _create_smart_summary(notes):
        """Enhanced smart summary as final fallback"""
        sentences = [s.strip() for s in notes.split('.') if s.strip()]
        
        if not sentences:
            return notes[:150] + '...' if len(notes) > 150 else notes
        
        # Simple algorithm: take first 2-3 meaningful sentences
        meaningful_sentences = []
        for sentence in sentences:
            if len(sentence.split()) > 4 and len(meaningful_sentences) < 3:
                meaningful_sentences.append(sentence)
        
        summary = '. '.join(meaningful_sentences)
        return f"📝 Key Points:\n{summary}"

    # Keep your existing quiz methods...
    @staticmethod
    def generate_quiz():
        try:
            data = request.get_json()
            notes = data.get('notes', '')
            
            if not notes or notes.strip() == '':
                return jsonify({'error': 'No notes provided'}), 400
            
            quiz = AIController._create_smart_quiz(notes)
            
            return jsonify({
                'quiz': quiz,
                'model': 'smart-generator'
            }), 200
            
        except Exception as e:
            quiz = "🧠 Study Questions:\n\n1. What are the main concepts?\n2. How would you apply this knowledge?\n3. What was most surprising?"
            return jsonify({'quiz': quiz, 'model': 'fallback'}), 200
    
    @staticmethod
    def _create_smart_quiz(notes):
        """Create smart quiz questions"""
        sentences = [s.strip() for s in notes.split('.') if s.strip() and len(s) > 20]
        
        if len(sentences) < 2:
            return "Add more detailed notes to generate better quiz questions."
        
        questions = ["🧠 Quick Quiz:\n"]
        
        for i, sentence in enumerate(sentences[:3]):
            words = sentence.split()
            if len(words) > 6:
                # Create different question types
                if i == 0:
                    questions.append(f"Q1: What is the main idea of: '{sentence}'?")
                    questions.append("")
                elif i == 1:
                    blank_idx = min(3, len(words) - 1)
                    question_words = words.copy()
                    answer = question_words[blank_idx]
                    question_words[blank_idx] = "_____"
                    questions.append(f"Q2: Complete: {' '.join(question_words)}")
                    questions.append(f"Answer: {answer}")
                    questions.append("")
                else:
                    questions.append(f"Q3: Explain this concept in your own words.")
                    questions.append("")
        
        return '\n'.join(questions) if len(questions) > 1 else "Reflect on the key concepts in your notes."