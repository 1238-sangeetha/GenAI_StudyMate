# GenAI_StudyMate-

---

# ⚙️ Backend Files  

### `backend/granite_ai.py`
```python
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import easyocr

class GraniteAIApp:
    def __init__(self):
        print("🔄 Loading Granite model...")
        self.model_name = "ibm-granite/granite-3.3-2b-instruct"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            low_cpu_mem_usage=True
        ).to(self.device)

        self.ocr_reader = easyocr.Reader(['en'])
        print("✅ Granite model ready!")

    def generate_response(self, prompt, max_tokens=400):
        inputs = self.tokenizer(prompt, return_tensors="pt",
                                truncation=True, max_length=1024, padding=True)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id
            )
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response[len(prompt):].strip()


