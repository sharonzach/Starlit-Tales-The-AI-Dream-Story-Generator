import gradio as gr
from transformers import pipeline

# Load GPT-2 model with longer output
story_gen = pipeline(
    "text-generation",
    model="gpt2",
    max_new_tokens=250,        # Around 150–200 words
    do_sample=True,
    temperature=1.0,
    pad_token_id=50256         # Avoid warnings
)

# Story generation function
def generate_story(prompt, creativity):
    if not prompt.strip():
        return "✨ Please enter a magical prompt to begin your story!"
    
    result = story_gen(prompt, do_sample=True, temperature=creativity)
    story = result[0]['generated_text']

    # Optional: Try to end neatly at sentence end
    if "." in story:
        story = story.rsplit(".", 1)[0] + "."

    return story

# Custom CSS with background image from Imgur
custom_css = """
body {
    background-image: url('https://i.imgur.com/Nh9EvX5.jpg');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    font-family: 'Comic Sans MS', cursive, sans-serif;
    color: white;
    margin: 0;
    padding: 0;
}

.gradio-container {
    background-color: rgba(0, 0, 50, 0.6) !important;
    border-radius: 20px;
    padding: 30px;
}

textarea, input[type="text"] {
    background-color: rgba(0, 0, 100, 0.3) !important;
    color: #ffffff !important;
    border-radius: 10px;
    border: none;
    font-size: 16px;
}

button {
    background-color: #ffcc70 !important;
    color: black !important;
    font-weight: bold;
    border-radius: 12px;
    padding: 10px 20px;
    font-size: 18px;
}

.slider {
    background-color: rgba(0, 0, 100, 0.3) !important;
}
"""

# Gradio UI
with gr.Blocks(css=custom_css) as demo:
    gr.Markdown("""
    <div style="text-align: center; font-size: 30px; font-weight: bold; color: #fff;">
        🌙✨ Starlit Tales: The AI Dream Story Generator ✨🌙
    </div>
    <div style="text-align: center; color: #eee; font-size: 18px;">
        Let your imagination soar through galaxies, dreams, and fairy tales...  
        Just give a magical prompt and watch your story come to life!
    </div>
    """)

    with gr.Row():
        prompt = gr.Textbox(label="🌟 Your Magical Prompt", placeholder="Once upon a time in a glowing cloud city...", lines=2)
        creativity = gr.Slider(label="🎨 Creativity Level", minimum=0.5, maximum=1.5, value=1.0, step=0.1)

    generate_btn = gr.Button("🚀 Tell Me a Story")
    output = gr.Textbox(label="📖 Your Dreamy Story", lines=12)

    generate_btn.click(fn=generate_story, inputs=[prompt, creativity], outputs=output)

# Run app
demo.launch(share=True)
