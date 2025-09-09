from frontend.ui import launch_ui

# Entry point for the Granite AI Learning Assistant
if __name__ == "__main__":
    demo = launch_ui()
    demo.launch(
        server_name="0.0.0.0",   # allows access from other devices (LAN)
        server_port=7860,        # default Gradio port
        share=True,              # generates public shareable link
        debug=True               # useful for error tracking
    )
