from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.core.text import LabelBase  # For custom fonts

import arabic_reshaper
from bidi.algorithm import get_display
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# Register the Arabic-supporting font
LabelBase.register(name='Tajawal', fn_regular='Tajawal-Regular.ttf')

Window.size = (600, 420)
Window.clearcolor = (0.1, 0.1, 0.1, 1)
language = "en"

def reshape_text(text):
    """Prepare Arabic text for RTL display."""
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

def toggle_language(instance):
    global language
    language = "ar" if language == "en" else "en"
    set_labels()

def set_labels():
    if language == "ar":
        app.label.text = reshape_text("ادخل الداله البيانية: مثل \nx^2+4")
        app.label.halign = 'right'
        app.button_plot.text = reshape_text("رسم الدالة")
        app.button_lang.text = reshape_text("تغيير اللغة")
        app.label_result.text = ""
    else:
        app.label.text = "Enter a mathematical function for x (eg. x^2+4):"
        app.label.halign = 'center'
        app.button_plot.text = "Plot Function"
        app.button_lang.text = "Change Language"
        app.label_result.text = ""

def plot_function(instance):
    func_str = app.text_input.text
    output.text = ""
    try:
        x = sp.symbols('x')
        func = sp.sympify(func_str)
        func_numeric = sp.lambdify(x, func, 'numpy')
        x_vals = np.linspace(-10, 10, 400)
        y_vals = func_numeric(x_vals)
        fig, ax = plt.subplots()
        ax.plot(x_vals, y_vals, label=f'f(x) = {func_str}', color='cyan')
        ax.axhline(0, color='white', linewidth=1)
        ax.axvline(0, color='white', linewidth=1)
        title_text = 'Function Plot' if language == 'en' else reshape_text('تمثيل بياني للدالة')
        ax.set_title(title_text, color='white')
        ax.set_xlabel('x', color='white')
        ax.set_ylabel('f(x)', color='white')
        ax.grid(True, color='gray')
        ax.legend()
        ax.set_ylim(-10, 20)
        ax.set_xlim(-20, 20)
        ax.set_facecolor('black')
        plt.show()
    except Exception:
        error_message = "[x]: Invalid Operation | لا يمكنك اجراء هذه العمليه"
        app.label_result.text = reshape_text(error_message)

class FunctionPlotterApp(App):
    def build(self):
        global app
        app = self
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)

        with layout.canvas.before:
            Color(0.15, 0.15, 0.15, 0.9)
            self.bg_rect = RoundedRectangle(size=layout.size, pos=layout.pos, radius=[20])
        layout.bind(size=self._update_rect, pos=self._update_rect)

        self.label = Label(
            text="Enter a mathematical function for x (eg. x^2+4):",
            color=(1, 1, 1, 1), size_hint_y=None, height=40, font_size=18, halign='center',
            valign='middle', font_name='Tajawal'
        )
        layout.add_widget(self.label)

        self.text_input = TextInput(
            size_hint_y=None, height=40, multiline=False, background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1), padding=[10, 10], font_size=16
        )
        layout.add_widget(self.text_input)

        self.button_plot = Button(
            text="Plot Function", size_hint_y=None, height=50,
            background_color=(0, 0.7, 1, 1), color=(1, 1, 1, 1), font_size=16, font_name='Tajawal'
        )
        self.button_plot.bind(on_press=plot_function)
        layout.add_widget(self.button_plot)

        self.button_lang = Button(
            text="Change Language", size_hint_y=None, height=50,
            background_color=(0, 0.7, 1, 1), color=(1, 1, 1, 1), font_size=16, font_name='Tajawal'
        )
        self.button_lang.bind(on_press=toggle_language)
        layout.add_widget(self.button_lang)
        
        self.label_result = Label(
            text="", color=(1, 0.2, 0.2, 1), size_hint_y=None, height=40, font_size=16, font_name='Tajawal'
        )
        layout.add_widget(self.label_result)

        global output
        output= self.label_result

        self.title = "f(x) finder | موجد الاقتران التربيعي | by M.Alghoul | بإشراف الأستاذ احمد الفليفل"
        return layout

    def _update_rect(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

if __name__ == '__main__':
    FunctionPlotterApp().run()
