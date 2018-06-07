# Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/components/session_navigation.py
# Compiled at: 2018-04-23 20:27:04
from __future__ import absolute_import, print_function, unicode_literals
from ...base import listens
from ..compound_component import CompoundComponent
from .scroll import ScrollComponent, Scrollable

class SessionRingScroller(Scrollable):

    def __init__(self, session_ring=None, *a, **k):
        super(SessionRingScroller, self).__init__(*a, **k)
        assert session_ring is not None
        self._session_ring = session_ring
        return

    do_scroll_up = NotImplemented
    do_scroll_down = NotImplemented

    def scroll_up(self):
        if self.can_scroll_up():
            self.do_scroll_up()

    def scroll_down(self):
        if self.can_scroll_down():
            self.do_scroll_down()


class SessionRingTrackScroller(SessionRingScroller):

    def can_scroll_up(self):
        return self._session_ring.track_offset > 0

    def can_scroll_down(self):
        return self._session_ring.track_offset + 1 < len(self._session_ring.tracks_to_use())

    def do_scroll_up(self):
        self._session_ring.move(-1, 0)

    def do_scroll_down(self):
        self._session_ring.move(1, 0)


class SessionRingSceneScroller(SessionRingScroller):

    def can_scroll_up(self):
        return self._session_ring.scene_offset > 0

    def can_scroll_down(self):
        return self._session_ring.scene_offset + 1 < len(self._session_ring.scenes())

    def do_scroll_up(self):
        self._session_ring.move(0, -1)

    def do_scroll_down(self):
        self._session_ring.move(0, 1)


class SessionRingTrackPager(SessionRingScroller):

    def __init__(self, *a, **k):
        super(SessionRingTrackPager, self).__init__(*a, **k)
        self.page_size = self._session_ring.num_tracks

    def can_scroll_up(self):
        return self._session_ring.track_offset > 0

    def can_scroll_down(self):
        return self._session_ring.track_offset < len(self._session_ring.tracks_to_use()) - self.page_size

    def do_scroll_up(self):
        self._session_ring.set_offsets(max(0, self._session_ring.track_offset - self.page_size), self._session_ring.scene_offset)

    def do_scroll_down(self):
        self._session_ring.set_offsets(self._session_ring.track_offset + self.page_size, self._session_ring.scene_offset)


class SessionRingScenePager(SessionRingScroller):

    def __init__(self, *a, **k):
        super(SessionRingScenePager, self).__init__(*a, **k)
        self.page_size = self._session_ring.num_scenes

    def can_scroll_up(self):
        return self._session_ring.scene_offset > 0

    def can_scroll_down(self):
        return self._session_ring.scene_offset < len(self._session_ring.scenes()) - self.page_size

    def do_scroll_up(self):
        self._session_ring.set_offsets(self._session_ring.track_offset, max(0, self._session_ring.scene_offset - self.page_size))

    def do_scroll_down(self):
        self._session_ring.set_offsets(self._session_ring.track_offset, self._session_ring.scene_offset + self.page_size)


class SessionNavigationComponent(CompoundComponent):
    u"""
    Allows moving the session ring using navigation controls.
    """
    track_scroller_type = SessionRingTrackScroller
    scene_scroller_type = SessionRingSceneScroller
    track_pager_type = SessionRingTrackPager
    scene_pager_type = SessionRingScenePager

    def __init__(self, session_ring=None, *a, **k):
        super(SessionNavigationComponent, self).__init__(*a, **k)
        assert session_ring is not None
        self._session_ring = session_ring
        self.__on_offset_changed.subject = self._session_ring
        self.__on_tracks_changed.subject = self._session_ring
        self.__on_scene_list_changed.subject = self.song
        self._vertical_banking, self._horizontal_banking, self._vertical_paginator, self._horizontal_paginator = self.register_components(ScrollComponent(self.scene_scroller_type(session_ring)), ScrollComponent(self.track_scroller_type(session_ring)), ScrollComponent(self.scene_pager_type(session_ring)), ScrollComponent(self.track_pager_type(session_ring)))
        return

    @listens('offset')
    def __on_offset_changed(self, track_offset, _):
        self._update_vertical()
        self._update_horizontal()

    @listens('tracks')
    def __on_tracks_changed(self):
        self._update_horizontal()

    @listens('scenes')
    def __on_scene_list_changed(self):
        self._update_vertical()

    def _update_vertical(self):
        if self.is_enabled():
            self._vertical_banking.update()
            self._vertical_paginator.update()

    def _update_horizontal(self):
        if self.is_enabled():
            self._horizontal_banking.update()
            self._horizontal_paginator.update()

    def set_up_button(self, button):
        self._vertical_banking.set_scroll_up_button(button)

    def set_down_button(self, button):
        self._vertical_banking.set_scroll_down_button(button)

    def set_left_button(self, button):
        self._horizontal_banking.set_scroll_up_button(button)
        self._horizontal_banking.update()

    def set_right_button(self, button):
        self._horizontal_banking.set_scroll_down_button(button)

    def set_page_up_button(self, page_up_button):
        self._vertical_paginator.set_scroll_up_button(page_up_button)

    def set_page_down_button(self, page_down_button):
        self._vertical_paginator.set_scroll_down_button(page_down_button)

    def set_page_left_button(self, page_left_button):
        self._horizontal_paginator.set_scroll_up_button(page_left_button)

    def set_page_right_button(self, page_right_button):
        self._horizontal_paginator.set_scroll_down_button(page_right_button)
