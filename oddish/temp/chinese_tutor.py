from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import time
import torch
import json

# Load Chinese-capable model
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # Keep the working model for now
model_name = "Qwen/Qwen2-1.5B-Instruct"

def load_model():
    """Load model with GPU optimization"""
    print("Loading model...")
    ts = time.time()
    
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        
        # Add padding token if missing
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        model_kwargs = {
            'torch_dtype': torch.float16,
            'device_map': "auto",
            'use_cache': True,
            'low_cpu_mem_usage': True,
            'trust_remote_code': True
        }
        
        model = AutoModelForCausalLM.from_pretrained(model_name, **model_kwargs)
        print(f'Model loaded in {time.time() - ts:.2f} seconds')
        
        return tokenizer, model
        
    except Exception as e:
        print(f"Error loading model: {e}")
        print("Falling back to TinyLlama...")
        
        # Fallback to working model
        fallback_model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        tokenizer = AutoTokenizer.from_pretrained(fallback_model, trust_remote_code=True)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
            
        model = AutoModelForCausalLM.from_pretrained(
            fallback_model,
            torch_dtype=torch.float16,
            device_map="auto",
            use_cache=True,
            low_cpu_mem_usage=True,
            trust_remote_code=True
        )
        print(f'Fallback model loaded in {time.time() - ts:.2f} seconds')
        return tokenizer, model

def parse_json_output(text, target_word):
    """Parse and clean the JSON output from the model"""
    try:
        # Try to find JSON in the text
        start_idx = text.find('{')
        end_idx = text.rfind('}') + 1
        
        if start_idx != -1 and end_idx != 0:
            json_str = text[start_idx:end_idx]
            lesson_data = json.loads(json_str)
            
            # Validate required fields
            required_fields = ['target_word', 'sentences', 'question', 'options', 'correct_answer']
            if all(field in lesson_data for field in required_fields):
                return lesson_data
            else:
                print("Missing required fields in JSON")
                return None
        else:
            print("No valid JSON found in output")
            return None
            
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        return None
    except Exception as e:
        print(f"Error parsing output: {e}")
        return None

def create_fallback_lesson(target_word, sentences_text):
    """Create a structured lesson when JSON parsing fails"""
    return {
        "target_word": target_word,
        "sentences": sentences_text.split('\n')[:3],
        "question": f"这些句子中，{target_word}起什么作用？",
        "options": [
            f"句子描述了与{target_word}相关的情况",
            "句子与天气无关",
            "句子描述了相反的情况"
        ],
        "correct_answer": 0,
        "explanation": f"句子中使用了{target_word}来描述相关的情景。",
        "note": "Fallback lesson generated due to parsing error"
    }

def create_chinese_lesson_prompt(word):
    """Create a structured prompt for Chinese learning"""
    return f"""请用词语"{word}"创建一个中文学习练习，以JSON格式输出。

格式示例：
{{
  "target_word": "晴天",
  "sentences": [
    "今天是晴天，太阳很大。",
    "我和朋友们去公园玩。",
    "我们很开心，因为天气很好。"
  ],
  "question": "为什么他们去公园玩？",
  "options": [
    "因为今天是晴天，天气很好。",
    "因为今天下雨了。",
    "因为今天很冷。"
  ],
  "correct_answer": 0,
  "explanation": "因为句子中说今天是晴天，天气很好，所以他们去公园玩。"
}}

现在请用词语"{word}"按相同JSON格式创建练习（只输出JSON，不要其他文字）："""

def save_lesson_to_file(lesson_data, target_word):
    """Save the lesson data to a JSON file"""
    filename = f"chinese_lesson_{target_word}.json"
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(lesson_data, f, ensure_ascii=False, indent=2)
        print(f"\nLesson saved to: {filename}")
    except Exception as e:
        print(f"Error saving file: {e}")

def main():
    # Check GPU
    if torch.cuda.is_available():
        print(f"Using GPU: {torch.cuda.get_device_name(0)}")
        torch.cuda.empty_cache()
    else:
        print("No GPU available - will be slower")
    
    # Load model
    tokenizer, model = load_model()
    
    # Create pipeline
    generator = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True
    )
    
    # Chinese word to practice
    target_word = "下雨"  # Try a different word
    
    # Create lesson
    prompt = create_chinese_lesson_prompt(target_word)

    print(prompt)
    
    print(f"\nGenerating Chinese lesson for: {target_word}")
    ts = time.time()
    
    try:
        result = generator(
            prompt,
            max_new_tokens=400,  # Increased for JSON output
            do_sample=True,
            temperature=0.3,
            top_p=0.8,
            pad_token_id=tokenizer.eos_token_id,
            return_full_text=False,
            repetition_penalty=1.1
        )
        
        generation_time = time.time() - ts
        print(f'Generation time: {generation_time:.2f} seconds')
        
        # Parse the JSON output
        raw_output = result[0]["generated_text"]
        lesson_data = parse_json_output(raw_output, target_word)
        
        if lesson_data:
            print("\n" + "="*50)
            print("CHINESE LESSON (JSON)")
            print("="*50)
            print(json.dumps(lesson_data, ensure_ascii=False, indent=2))
            
            print("\n" + "="*50)
            print("FORMATTED LESSON")
            print("="*50)
            print(f"词语: {lesson_data['target_word']}")
            print("\n句子:")
            for i, sentence in enumerate(lesson_data['sentences'], 1):
                print(f"{i}. {sentence}")
            
            print(f"\n问题: {lesson_data['question']}")
            print("\n选项:")
            for i, option in enumerate(lesson_data['options']):
                letter = chr(65 + i)  # A, B, C...
                print(f"{letter}. {option}")
            
            correct_letter = chr(65 + lesson_data['correct_answer'])
            print(f"\n答案: {correct_letter}")
            
            if 'explanation' in lesson_data:
                print(f"解释: {lesson_data['explanation']}")
            
            # Save to file
            save_lesson_to_file(lesson_data, target_word)
                
        else:
            print("Failed to parse JSON, showing raw output:")
            print(raw_output)
            
            # Create fallback lesson
            fallback_lesson = create_fallback_lesson(target_word, raw_output)
            print("\nFallback lesson:")
            print(json.dumps(fallback_lesson, ensure_ascii=False, indent=2))
            save_lesson_to_file(fallback_lesson, target_word)
        
    except Exception as e:
        print(f"Generation error: {e}")
        print("Trying with simpler parameters...")
        
        # Simpler fallback generation
        result = generator(
            f"用'{target_word}'造三个简单的中文句子：",
            max_new_tokens=100,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
            return_full_text=False
        )
        
        generation_time = time.time() - ts
        print(f'Generation time: {generation_time:.2f} seconds')
        
        # Create structured fallback
        fallback_lesson = create_fallback_lesson(target_word, result[0]["generated_text"])
        print("\nFallback lesson (JSON):")
        print(json.dumps(fallback_lesson, ensure_ascii=False, indent=2))
        save_lesson_to_file(fallback_lesson, target_word)
    
    # Performance info
    if torch.cuda.is_available():
        gpu_memory = torch.cuda.memory_allocated() / 1024**2
        print(f"\nGPU Memory Used: {gpu_memory:.1f} MB")

if __name__ == "__main__":
    main()
