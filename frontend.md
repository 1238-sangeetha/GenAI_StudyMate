# GenAI_StudyMate
import gradio as gr
from backend.granite_ai import GraniteAIApp
from backend.utils_pdf import extract_text_from_pdf
from backend.utils_ocr import extract_text_from_image
from backend.utils_ppt import create_ppt
from backend.utils_tts import generate_tts
from backend.utils_dict import build_dict_prompt

app = GraniteAIApp()

def launch_ui():
    with gr.Blocks(title="🤖 Granite AI Assistant") as demo:
        gr.Markdown("## 📘 Granite AI Learning Assistant")

        with gr.Tabs():
            with gr.Tab("📝 Notes"):
                pdf = gr.File(label="Upload PDF")
                query = gr.Textbox(label="Topic")
                output = gr.Textbox(label="Notes", lines=10)
                btn = gr.Button("Generate Notes")
                btn.click(lambda f, q: app.generate_response(extract_text_from_pdf(f)+q), [pdf, query], output)

            with gr.Tab("📊 PPT Generator"):
                topic = gr.Textbox(label="Topic")
                ppt_out = gr.File(label="Download PPT")
                btn_ppt = gr.Button("Generate PPT")
                btn_ppt.click(lambda t: create_ppt([{"title":t, "content":app.generate_response(f"Make slides on {t}")}]), topic, ppt_out)

            with gr.Tab("📖 Explainer"):
                q = gr.Textbox(label="Question")
                a = gr.Textbox(label="Answer", lines=8)
                btn_exp = gr.Button("Explain")
                btn_exp.click(lambda x: app.generate_response(f"Explain in detail: {x}"), q, a)

            with gr.Tab("🎴 Flashcards"):
                topic = gr.Textbox(label="Topic")
                cards = gr.Textbox(label="Flashcards", lines=8)
                btn_cards = gr.Button("Generate Flashcards")
                btn_cards.click(lambda t: app.generate_response(f"Make 5 flashcards on {t}"), topic, cards)

            with gr.Tab("🔊 Text-to-Speech"):
                text = gr.Textbox(label="Enter text")
                audio = gr.Audio(label="Speech", type="filepath")
                btn_tts = gr.Button("Convert to Audio")
                btn_tts.click(generate_tts, text, audio)

            with gr.Tab("📚 Dictionary"):
                word = gr.Textbox(label="Word")
                ctx = gr.Textbox(label="Context (optional)")
                result = gr.Textbox(label="Meaning", lines=8)
                btn_dict = gr.Button("Define")
                btn_dict.click(lambda w, c: app.generate_response(build_dict_prompt(w, c, "English")), [word, ctx], result)

            with gr.Tab("🗣 Pronunciation"):
                word = gr.Textbox(label="Word")
                audio = gr.Audio(label="Pronunciation", type="filepath")
                btn_pron = gr.Button("Hear")
                btn_pron.click(generate_tts, word, audio)

    return demo
