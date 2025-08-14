from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import time
import torch

# Check GPU availability
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")

# Load model
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

print("Loading model...")
ts = time.time()

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto",
    use_cache=True,
    low_cpu_mem_usage=True,
    trust_remote_code=True
)

print(f'Model loaded in {time.time() - ts:.2f} seconds')

# Create pipeline
generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    torch_dtype=torch.float16,
    device_map="auto",
    trust_remote_code=True
)

if torch.cuda.is_available():
    torch.cuda.empty_cache()
    print(f"GPU memory: {torch.cuda.memory_allocated() / 1024**2:.1f} MB")

# Chinese lesson prompt
def create_chinese_lesson_prompt(word):
    return f"""Create a Chinese learning lesson using the word '{word}'. Follow this exact format:

Three simple sentences using '{word}':

今天是晴天，太阳很大。
我和朋友们去公园玩。
我们很开心，因为天气很好。

问题：
故事里，为什么"我"和朋友们去公园玩？

A. 因为今天是晴天，天气很好。
B. 因为今天下雨了。
C. 因为今天很冷。

Use simple HSK 1-2 level vocabulary. Make sentences tell a connected story."""

# Generate Chinese lesson
target_word = "晴天"
prompt = create_chinese_lesson_prompt(target_word)

print(f"\nGenerating lesson for: {target_word}")
ts = time.time()

result = generator(
    prompt,
    max_new_tokens=200,
    do_sample=True,
    temperature=0.7,
    top_p=0.9,
    pad_token_id=tokenizer.eos_token_id,
    return_full_text=False
)

print(f'Generation time: {time.time() - ts:.2f} seconds')
print("\n" + "="*50)
print("CHINESE LESSON")
print("="*50)
print(result[0]["generated_text"])