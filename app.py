import gradio as gr
import google.generativeai as genai
import os

# ✅ Configure Gemini API key
genai.configure(api_key="")
model = genai.GenerativeModel("gemini-2.0-flash")

# 🧠 Bot logic
def medical_chatbot(symptoms, duration, severity):
    prompt = f"""
    You are a virtual health assistant providing general health information.
    diagnosis the user might have based on their symptoms.
    The user reports:
    Symptoms: {symptoms}
    Duration: {duration}
    Severity: {severity}

    Please provide:
    diagnosis
    - General care or over-the-counter remedies
    - Advice on when to see a doctor
    - Warm, friendly tone

    Add: "⚠️ This is not medical advice. Please consult a healthcare provider."
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ An error occurred: {e}"

# 🎨 Build fancy UI with Blocks
with gr.Blocks(theme=gr.themes.Base(), css=".gradio-container {font-family: 'Segoe UI', sans-serif;}") as demo:
    gr.Markdown("## 🩺 AI Medical Assistant Chatbot")
    gr.Markdown("Get general health guidance based on your symptoms. ⚠️ *This is not medical advice.*")

    with gr.Row():
        symptoms = gr.Textbox(lines=3, label="Describe your symptoms", placeholder="e.g. fever, sore throat, fatigue...")
        duration = gr.Dropdown(["< 1 day", "1–3 days", "4–7 days", "Over a week"], label="How long have you had these symptoms?")
        severity = gr.Radio(["Mild", "Moderate", "Severe"], label="How severe are your symptoms?")

    submit_btn = gr.Button("🩺 Get Health Info")
    output = gr.Textbox(label="AI Medical Advice", lines=10)
    clear_btn = gr.Button("🔄 Reset")

    submit_btn.click(fn=medical_chatbot, inputs=[symptoms, duration, severity], outputs=output)
    clear_btn.click(fn=lambda: ("", None, None, ""), inputs=[], outputs=[symptoms, duration, severity, output])

# 🚀 Launch
if __name__ == "__main__":
    demo.launch()
