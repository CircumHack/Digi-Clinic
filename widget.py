from kivymd.uix.bottomsheet import MDCustomBottomSheet
from kivy.uix.modalview import ModalView
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.dialog import BaseDialog
from kivycupertino.uix.textfield import CupertinoTextField
from kivymd.uix.snackbar import BaseSnackbar
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import Clock
from kivymd.uix.behaviors import RectangularElevationBehavior
from kivy.core.window import Window
from kivy.properties import *
import datetime
class MySnackBar(BaseSnackbar):
      text=StringProperty(None)
      icon=StringProperty(None)
      font_size=NumericProperty('12sp')        
class CodeNum(CupertinoTextField):
    def insert_text(self, substring, from_undo = False):
        s = substring.upper().strip()
        if len(self.text) < self.max_text_length:
            return super(CodeNum, self).insert_text(s, from_undo = from_undo)
class HospitalButtom(MDCustomBottomSheet):
      def __init__(self, **kwargs):
            self.duration_opening=.01
            self.duration_closing=.01
            self.radius=10
            self.radius_from='top'
            super(HospitalButtom,self).__init__(**kwargs)
class HospitalList(OneLineIconListItem):
      icon = StringProperty()
class MyDialog(BaseDialog):
      dialog_radius = NumericProperty("15dp")
      bg_color = ListProperty()
      size_portrait = ListProperty(["250dp", "300dp"])
      size_landscape = ListProperty(["400dp", "300dp"])
      header_width_landscape = NumericProperty("120dp")
      header_height_portrait = NumericProperty("100dp")
      fixed_orientation = OptionProperty(None, options=["portrait", "landscape"])
      header_bg = ListProperty()
      header_text_type = OptionProperty("icon", options=["icon", "text"])
      header_text = StringProperty()
      header_icon = StringProperty("android")
      header_color = ListProperty()
      header_h_pos = StringProperty("center")
      header_v_pos = StringProperty("center")
      header_font_size = NumericProperty("60dp")
      progress_interval = NumericProperty(None)
      progress_width = NumericProperty("5dp")
      progress_color = ListProperty()
      elevation = NumericProperty(10)
      content_cls = ObjectProperty()
      opening_duration = NumericProperty(.1)
      dismiss_duration = NumericProperty(.1)
      _orientation = StringProperty()
      _progress_value = NumericProperty()
      def __init__(self, **kwargs):
            super(MyDialog,self).__init__(**kwargs)
            Window.bind(on_resize=self._get_orientation)
            self.register_event_type("on_progress_finish")
            Clock.schedule_once(self._update)
      def _update(self, *args):
            self._get_orientation()
            Window.bind(on_touch_down=self._window_touch_down)
            Window.bind(on_touch_up=self._window_touch_up)
            Window.bind(on_touch_move=self._window_touch_move)
      def _collide_point_with_modal(self, pos):
            if self.attach_to:
                  raise NotImplementedError
            for widget in Window.children:
                  if issubclass(widget.__class__, ModalView):
                        if widget.collide_point(pos[0], pos[1]):
                              return widget
                  return False

      def _get_top_modal(self):
            for widget in Window.children:
                  if issubclass(widget.__class__, ModalView):
                        return widget

      def on_touch_down(self, touch):
            pos = touch.pos
            if self.collide_point(pos[0], pos[1]):
                  return super().on_touch_down(touch)
            if self._get_top_modal() == self:
                  MDApp.get_running_app().root.dispatch("on_touch_down", touch)
            return super().on_touch_down(touch)

      def on_touch_up(self, touch):
            pos = touch.pos
            if self.collide_point(pos[0], pos[1]):
                  return super().on_touch_up(touch)
            if self._get_top_modal() == self:
                  MDApp.get_running_app().root.dispatch("on_touch_up", touch)
            return super().on_touch_up(touch)

      def on_touch_move(self, touch):
            pos = touch.pos
            if self.collide_point(pos[0], pos[1]):
                  return super().on_touch_move(touch)
            if self._get_top_modal() == self:
                  MDApp.get_running_app().root.dispatch("on_touch_move", touch)
            return super().on_touch_move(touch)

      def _window_touch_down(self, instance, touch):
            pos = touch.pos
            collide_modal = self._collide_point_with_modal(pos)
            if collide_modal == self and self._get_top_modal == self:
                  return
            if collide_modal == self and self._get_top_modal != self:
                  return collide_modal.dispatch("on_touch_down", touch)

      def _window_touch_up(self, instance, touch):
            pos = touch.pos
            collide_modal = self._collide_point_with_modal(pos)
            if collide_modal == self and self._get_top_modal == self:
                  return
            if collide_modal == self and self._get_top_modal != self:
                  return collide_modal.dispatch("on_touch_up", touch)

      def _window_touch_move(self, instance, touch):
            pos = touch.pos
            collide_modal = self._collide_point_with_modal(pos)
            if collide_modal == self and self._get_top_modal == self:
                  return
            if collide_modal == self and self._get_top_modal != self:
                  return collide_modal.dispatch("on_touch_move", touch)

      def _get_orientation(self, *args):
            if self.fixed_orientation:
                  self._orientation = self.fixed_orientation
            elif self.theme_cls.device_orientation == "portrait":
                  self._orientation = "portrait"
            else:
                  self._orientation = "landscape"

      def on_content_cls(self, *args):
            if not self.content_cls:
                  return

            self.ids.content.clear_widgets()
            self.ids.content.add_widget(self.content_cls)

      def on_open(self):
            self._start_progress()
            return super().on_open()

      def on_pre_open(self):
            self._opening_animation()
            return super().on_pre_open()

      def on_dismiss(self):
            self._dismiss_animation()
            return super().on_dismiss()

      def _opening_animation(self):
            self.opacity = 0
            anim = Animation(
                  opacity=1, duration=self.opening_duration, t="out_quad"
            )
            anim.start(self)

      def _dismiss_animation(self):
            anim = Animation(
                  opacity=0, duration=self.dismiss_duration, t="out_quad"
            )
            anim.start(self)

      def _start_progress(self):
            if not self.progress_interval:
                  return
            max_width = self.size[0] - self.dialog_radius * 2
            anim = Animation(
                  _progress_value=max_width, duration=self.progress_interval
            )
            anim.bind(on_complete=lambda x, y: self.dispatch("on_progress_finish"))
            anim.start(self)

      def on_progress_finish(self, *args):
            pass
class MainAlert(RectangularElevationBehavior,MDBoxLayout):
      pass
