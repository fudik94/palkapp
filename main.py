#btw its my first amateur project thats why dont judge!bir sozle qinamayin.
#my name is Fuad094
#agilli ol..

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.graphics.texture import Texture

import matplotlib.pyplot as plt
import io


translations = {
    'en': {
        'input_hint': "Enter gross salary (€)",
        'calculate': "Calculate",
        'net': "Net salary",
        'taxes': "Total taxes",
        'error': "Error: enter a number",
        'income_tax': "Income tax",
        'pension': "II pillar",
        'chart_title': "Salary distribution",
        'footer': "© 2025 PalkApp. All rights reserved.\nQuestions or feedback: palkapp.info@gmail.com"
    },
    'ru': {
        'input_hint': "Введите брутто-зарплату (€)",
        'calculate': "Рассчитать",
        'net': "Чистыми",
        'taxes': "Налоги",
        'error': "Ошибка: введите число",
        'income_tax': "Подоходный налог",
        'pension': "II пенсионный столб",
        'chart_title': "Распределение зарплаты",
        'footer': "© 2025 PalkApp. Все права защищены.\nВопросы или предложения: palkapp.info@gmail.com"
    },
    'et': {
        'input_hint': "Sisesta brutopalk (€)",
        'calculate': "Arvuta",
        'net': "Netopalk",
        'taxes': "Maksud",
        'error': "Viga: sisesta number",
        'income_tax': "Tulumaks",
        'pension': "II pensioni sammas",
        'chart_title': "Palga jaotus",
        'footer': "© 2025 PalkApp. Kõik õigused kaitstud.\nKüsimused või tagasiside: palkapp.info@gmail.com"
    }
}


class SalaryCalculator(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_lang = 'ru'
        self.build_ui()

    def build_ui(self):
        self.layout = MDBoxLayout(orientation='vertical', padding=20, spacing=15)

        lang_layout = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=40)
        for lang_code in ['ru', 'en', 'et']:
            btn = MDFlatButton(
                text=lang_code.upper(),
                on_release=lambda x, code=lang_code: self.change_language(code),
            )
            lang_layout.add_widget(btn)
        self.layout.add_widget(lang_layout)

        self.salary_input = MDTextField(
            hint_text="",
            mode="rectangle",
            input_filter="float",
        )
        self.layout.add_widget(self.salary_input)

        self.calc_button = MDRaisedButton(
            text="",
            on_release=self.calculate_salary,
            pos_hint={"center_x": 0.5},
        )
        self.layout.add_widget(self.calc_button)

        self.result_label = MDLabel(
            text="",
            halign="center",
            theme_text_color="Primary",
            markup=True,
            size_hint_y=None,
            height=100
        )
        self.layout.add_widget(self.result_label)

        self.chart_image = Image(size_hint_y=0.6)
        self.layout.add_widget(self.chart_image)

        self.footer_label = MDLabel(
            text="",
            halign="center",
            theme_text_color="Secondary",
            font_style="Caption",
            size_hint_y=None,
            height=60,
        )
        self.layout.add_widget(self.footer_label)

        self.add_widget(self.layout)
        self.change_language(self.current_lang)

    def change_language(self, lang_code):
        self.current_lang = lang_code
        t = translations[lang_code]
        self.salary_input.hint_text = t['input_hint']
        self.salary_input.text = ""
        self.calc_button.text = t['calculate']
        self.result_label.text = ""
        self.chart_image.texture = None
        self.footer_label.text = t['footer']

    def calculate_salary(self, instance):
        t = translations[self.current_lang]
        try:
            gross = float(self.salary_input.text)
            pension = gross * 0.02

            if gross <= 1200:
                free_amount = 654
            elif gross > 2100:
                free_amount = 0
            else:
                free_amount = 654 - 654 / 900 * (gross - 1200)

            taxable_income = max(0, gross - free_amount)
            income_tax = taxable_income * 0.20
            net = gross - income_tax - pension

            self.result_label.text = (
                f"[b]{t['net']}: {net:.2f} €[/b]\n"
                f"{t['taxes']}: {(income_tax + pension):.2f} €\n"
                f"{t['income_tax']}: {income_tax:.2f} €, {t['pension']}: {pension:.2f} €"
            )

            self.create_pie_chart(net, income_tax, pension, t)

        except ValueError:
            self.result_label.text = t['error']
            self.chart_image.texture = None

    def create_pie_chart(self, net, income_tax, pension, t):
        labels = [
            f"{t['net']}: {net:.0f}€",
            f"{t['income_tax']}: {income_tax:.0f}€",
            f"{t['pension']}: {pension:.0f}€"
        ]
        sizes = [net, income_tax, pension]
        colors = ['#4caf50', '#f44336', '#2196f3']

        fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            textprops={'fontsize': 9, 'color': 'white'}
        )
        ax.set_title(t['chart_title'], fontsize=12)
        ax.axis('equal')

        # Легенда (вместо подписей внутри)
        ax.legend(wedges, labels, title=t['chart_title'], loc='lower center', bbox_to_anchor=(0.5, -0.1), fontsize=9)

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
        plt.close(fig)
        buf.seek(0)

        im = CoreImage(buf, ext="png")
        self.chart_image.texture = im.texture
        self.chart_image.canvas.ask_update()


class PalkApp(MDApp):
    def build(self):
        self.title = "PalkApp"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        return SalaryCalculator()


if __name__ == "__main__":
    PalkApp().run()
