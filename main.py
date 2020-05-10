from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.graphics import (Color, Ellipse, Rectangle, Line)
from kivy.core.window import Window

from time import time

from kivy.config import Config
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '900')
Config.set('graphics', 'minimum_width', '400')
Config.set('graphics', 'minimum_height', '900')

WIDTH_MENU = 150

class PainterWidget(Widget):
	def __init__(self, **kwargs):
		super(PainterWidget, self).__init__(**kwargs)
		self.rad = 5
		self.color_brush = (0, 0, 1, 1)
		self.color_paper = (1, 0, 1, 1)
		Color(*self.color_paper)
		self.rectangle = Rectangle(background_color = self.color_paper,
			pos=(200, 200), size=(200,200))

	def on_touch_down(self, touch):
		with self.canvas:
			Color(*self.color_brush)
			if touch.x > WIDTH_MENU + self.rad:
				Ellipse(pos=(touch.x - self.rad / 2, touch.y - self.rad / 2), size=(self.rad, self.rad))
				touch.ud['line'] = Line(points = (touch.x, touch.y), width = self.rad)

	def on_touch_move(self, touch):
		if touch.x > WIDTH_MENU + self.rad:
			if "line" in touch.ud:
				touch.ud['line'].points += (touch.x, touch.y)
			else:
				Ellipse(pos=(touch.x - self.rad / 2, touch.y - self.rad / 2), size=(self.rad, self.rad))
				touch.ud['line'] = Line(points = (touch.x, touch.y), width = self.rad)

class PaintApp(App):
    def build(self):
    	self.color_paper = (0, 1, 0, 1)

    	self.painter = painter = PainterWidget()
    	painter.bind(size=self._update_rect, pos=self._update_rect)

    	box_main = BoxLayout(orientation='horizontal', padding=0)
    	self.box_painter = box_painter = BoxLayout(orientation='horizontal', padding=0)
    	box_menu = BoxLayout(orientation='vertical', padding=5, spacing=5
    		, size_hint=(None, None), size=(WIDTH_MENU, 800))#, background_color = (1, 0, 0, 1)
    	grid_brush_color = GridLayout(cols=3, spacing=5
    		, size_hint=(None, None), size =(WIDTH_MENU, 180))
    	grid_paper_color = GridLayout(cols=3, spacing=5
    		, size_hint=(None, None), size =(WIDTH_MENU, 150))

    	label_brash = Label(text='Brush size', font_size=25
    		, halign='center', color = [1, 0, 1, 1], size_hint=(1, None), size =(100, 40))
    	slider = Slider(min=1, max=10, value=5, size_hint=(1, None), size =(100, 30)
    		, on_touch_move = self.on_slider_touch_move)
    	
    	label_color = Label(text='Brush color', font_size=25, halign='center'
    		, color = [1, 0, 1, 1], size_hint=(1, None), size =(100, 40))
    	label_paper = Label(text='Paper color', font_size=25, halign='center'
    		, color = [1, 0, 1, 1], size_hint=(1, None), size =(100, 40))
    	btn_clear = Button(text='Clear', font_size=25, background_normal=''
    		, background_color = [80/256, 25/256, 80/256, 1], border=(16, 16, 16, 16)
            , size_hint=(1, None), size =(100, 40)
            , on_press=self.on_clear_canvas)
    	btn_save = Button(text='Save', font_size=25, background_normal=''
    		, background_color = [57/256, 117/256, 73/256, 1], border=(16, 16, 16, 16)
            , size_hint=(1, None), size =(100, 40)
            , on_press=self.on_save)

    	box_menu.add_widget(label_brash)
    	box_menu.add_widget(slider)
    	box_menu.add_widget(label_color)
    	box_menu.add_widget(grid_brush_color)
    	box_menu.add_widget(label_paper)
    	box_menu.add_widget(grid_paper_color)
    	box_menu.add_widget(btn_clear)
    	box_menu.add_widget(btn_save)

    	colors = [[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1]
    			, [1, 1, 0, 1], [1, 0, 1, 1], [0, 1, 1, 1]
    			, [1, 1, 1, 1], [.5, 0, .5, 1], [.5, .5, .5, 1]
    			, [0, 0, 0, 1], [.25, .25, .25, 1], [.25, .75, .75, 1]
    			, [0, .4, .1, 1], [0, .25, .25, 1], [.2, .15, .75, 1]
    	]
    	for i in range(15):
    		grid_brush_color.add_widget(Button(background_color = colors[i]
    		, background_normal='', on_press=self.on_brush_color))

    	for i in range(12):
    		grid_paper_color.add_widget(Button(background_color = colors[i]
    		, background_normal='', on_press=self.on_paper_color))
    	
    	box_main.add_widget(box_menu)
    	box_painter.add_widget(painter)
    	box_main.add_widget(box_painter)
    	self.on_change_bg_color(self.color_paper)

    	return box_main

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_clear_canvas(self, instance):
    	self.painter.canvas.clear()

    def on_save(self, instance):
    	timestamp = str(int(time()))
    	self.painter.size = (Window.size[0], Window.size[1])
    	self.painter.parent.export_to_png("paint_{}.png".format(timestamp))

    def on_brush_color(self, instance):
    	self.painter.color_brush = instance.background_color

    def on_paper_color(self, instance):
    	self.on_change_bg_color(instance.background_color)

    def on_change_bg_color(self, color):
    	with self.box_painter.canvas.before:
    		Color(*color)
    		self.rect = Rectangle(size=self.painter.size, pos=self.painter.pos)

    def on_slider_touch_move(self, instance, touch):
    	self.painter.rad = int(instance.value)

if __name__ == "__main__":
    PaintApp().run()
