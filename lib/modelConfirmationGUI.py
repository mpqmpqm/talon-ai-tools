from talon import Module, actions, clip, imgui

from .modelHelpers import GPTState, notify

mod = Module()


@imgui.open()
def confirmation_gui(gui: imgui.GUI):
    gui.text("Confirm model output before pasting")
    gui.line()
    gui.spacer()
    for line in GPTState.text_to_confirm.split("\n"):
        gui.text(line)

    gui.spacer()
    if gui.button("Model paste output"):
        actions.user.paste_model_confirmation_gui()

    gui.spacer()
    if gui.button("Model copy output"):
        actions.user.copy_model_confirmation_gui()

    gui.spacer()
    if gui.button("Model discard output"):
        actions.user.close_model_confirmation_gui()


@mod.action_class
class UserActions:
    def add_to_confirmation_gui(model_output: str):
        """Add text to the confirmation gui"""
        GPTState.text_to_confirm = model_output
        confirmation_gui.show()

    def close_model_confirmation_gui():
        """Close the model output without pasting it"""
        GPTState.text_to_confirm = ""
        confirmation_gui.hide()

    def copy_model_confirmation_gui():
        """Copy the model output to the clipboard"""
        clip.set_text(GPTState.text_to_confirm)
        GPTState.text_to_confirm = ""

        confirmation_gui.hide()

    def paste_model_confirmation_gui():
        """Paste the model output"""
        if not GPTState.text_to_confirm:
            notify("GPT error: No text in confirmation GUI to paste")
            GPTState.text_to_confirm = ""
            confirmation_gui.hide()
            return
        else:
            actions.user.paste(GPTState.text_to_confirm)
            GPTState.text_to_confirm = ""
            confirmation_gui.hide()