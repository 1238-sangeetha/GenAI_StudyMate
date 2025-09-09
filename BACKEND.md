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
utils_ocr.py
import easyocr
ocr_reader = easyocr.Reader(['en'])

def extract_text_from_image(image_file):
    result = ocr_reader.readtext(image_file.name)
    return " ".join([text[1] for text in result])
utils_ppt.py
from pptx import Presentation
from pptx.util import Pt
import tempfile

def create_ppt(slides_data):
    prs = Presentation()
    for slide in slides_data:
        layout = prs.slide_layouts[1]
        slide_obj = prs.slides.add_slide(layout)
        slide_obj.shapes.title.text = slide['title']
        content = slide_obj.placeholders[1]
        content.text = slide['content']
        for p in content.text_frame.paragraphs:
            p.font.size = Pt(18)
    ppt_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pptx')
    prs.save(ppt_file.name)
    return ppt_file.name

backend/utils_tts.py
from gtts import gTTS
import tempfile

def generate_tts(text, lang="en"):
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        audio_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        tts.save(audio_file.name)
        return audio_file.name
    except:
        return None

backend/utils_dict.py
def build_dict_prompt(word, context, language):
    return f"""
Define the word "{word}" in {language}:
1. Definition
2. Part of speech
3. Synonyms & Antonyms
4. Etymology
5. Example sentence
6. Context meaning (from: {context[:200]})
"""



