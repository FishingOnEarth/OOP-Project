# Team members: Xuanchen Yu, Yiwen Ma, Jiaqi Sun
# Purpose: Handles the sliders and buttons and displays the observed frequency.

import pygame
from assets import load_image

#customize color
BACKGROUND_COLOR = (0, 0, 170)

COLOR_PALETTE = {
    "panel_bg": (0, 0, 130),
    "panel_border": (65, 70, 85),
    "title_text": (245, 245, 250),
    "label_text": (235, 235, 240),
    "slider_track": (0,0,0),
    "slider_fill": (255,165,0),
    "slider_knob": (255, 255, 0),
    "start_btn": (45, 165, 95),
    "pause_btn": (210, 140, 45),
    "reset_btn": (75, 82, 100),
    "btn_text": (255, 255, 255),
    "readout_bg": (0, 0, 0),
    "readout_text": (0, 255, 220),
}


class Slider:
    """Draggable horizontal slider for adjusting a numeric parameter."""

    def __init__(
        self,
        label,
        rect,
        min_val,
        max_val,
        initial_val,
        unit="",
        palette=None,
    ):
        """Set up the slider range, starting value, unit, and colors."""
        self.label = label
        self.rect = rect
        self.min_val = float(min_val)
        self.max_val = float(max_val)
        self.value = max(self.min_val, min(self.max_val, float(initial_val)))
        self.unit = unit
        self.dragging = False
        self.palette = palette if palette is not None else COLOR_PALETTE

    def _set_from_x(self, x):
        """Update the slider value based on a horizontal mouse position ratio with slider rectangle."""
        if self.rect.width <= 0:
            return
        ratio = (x - self.rect.x) / self.rect.width #ratio 
        ratio = max(0.0, min(1.0, ratio))
        self.value = self.min_val + ratio * (self.max_val - self.min_val) #linear interpolation method

    def handle_event(self, event):
        """Handle mouse clicks and drags on the slider and return if value changed."""
        changed = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            hit_box = self.rect.inflate(0, 12)
            if hit_box.collidepoint(event.pos):
                self.dragging = True
                self._set_from_x(event.pos[0])
                changed = True
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self._set_from_x(event.pos[0])
            changed = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging:
                self.dragging = False
                changed = True
        return changed

    def draw(self, screen, font):
        """Draw the slider label, value, track, filled bar, and knob."""
        # Label + current numeric value
        text_surf = font.render(
            f"{self.label}: {self.value:.1f} {self.unit}".strip(),
            True,
            self.palette["label_text"],
        )
        screen.blit(text_surf, (self.rect.x, self.rect.y - 20))

        # Track line
        pygame.draw.rect(
            screen, self.palette["slider_track"], self.rect, border_radius=4
        )

        # Filled portion + knob
        span = self.max_val - self.min_val
        ratio = 0.0 if span == 0 else (self.value - self.min_val) / span
        knob_x = int(self.rect.x + ratio * self.rect.width)
        filled_rect = pygame.Rect(
            self.rect.x, self.rect.y, max(0, knob_x - self.rect.x), self.rect.height
        )
        pygame.draw.rect(
            screen, self.palette["slider_fill"], filled_rect, border_radius=4
        )
        pygame.draw.circle(
            screen, self.palette["slider_knob"], (knob_x, self.rect.centery), 8
        )


class Interface:
    """Control panel managing sliders, buttons, and the observed frequency readout."""

    def __init__(
        self,
        panel_rect,
        base_freq=440.0,
        bg_color=BACKGROUND_COLOR,
        palette=None,
    ):
        """Build the control panel layout, buttons, sliders, and readout box."""
        self.panel_rect = panel_rect
        self.bg_color = bg_color
        self.palette = palette if palette is not None else COLOR_PALETTE

        self.font = pygame.font.SysFont("arial", 16)
        self.title_font = pygame.font.SysFont("arial", 18, bold=True)

        self.running = False
        self.reset_requested = False
        self.should_quit = False
        self.current_freq = float(base_freq)

        x = self.panel_rect.x + 16
        w = self.panel_rect.width - 32
        btn_w = (w - 10) // 2
        btn_h = 70
        bottom_margin = 16

        # Place Start/Pause and Reset buttons at the bottom of the panel/page
        btn_y = self.panel_rect.bottom - bottom_margin - btn_h
        self.start_pause_rect = pygame.Rect(x, btn_y, btn_w, btn_h)
        self.reset_rect = pygame.Rect(x + btn_w + 10, btn_y, btn_w, btn_h)

        #load images for buttons and title
        self.start_image = load_image("images/start.png", self.start_pause_rect.size)
        self.pause_image = load_image("images/pause.png", self.start_pause_rect.size)
        self.reset_image = load_image("images/reset.png", self.reset_rect.size)
        self.title_image = load_image("images/Title.png", (self.panel_rect.width - 8,240))
                
        # Sliders (speeds in m/s, base frequency in Hz)
        # Keep max speed safely below speed of sound (343 m/s)
        first_slider_y = self.panel_rect.top + 12 + self.title_image.get_height() + 20 + 12        
        self.source_speed_slider = Slider(
            "Source Speed",
            pygame.Rect(x, first_slider_y, w, 8),
            0.0,
            280.0,
            50.0,
            "m/s",
            palette=self.palette,
        )
        self.observer_speed_slider = Slider(
            "Observer Speed",
            pygame.Rect(x, first_slider_y+60, w, 8),
            0.0,
            280.0,
            0.0,
            "m/s",
            palette=self.palette,
        )
        self.base_freq_slider = Slider(
            "Base Freq (f0)",
            pygame.Rect(x, first_slider_y+120, w, 8),
            100.0,
            1200.0,
            base_freq,
            "Hz",
            palette=self.palette,
        )
        self.sliders = [
            self.source_speed_slider,
            self.observer_speed_slider,
            self.base_freq_slider,
        ]

        # Readout box positioned above the bottom buttons
        self.freq_box = pygame.Rect(x, btn_y - 58, w, 44)

    @property
    def source_speed(self):
        """Return the current source speed value from its slider."""
        return self.source_speed_slider.value

    @property
    def observer_speed(self):
        """Return the current observer speed value from its slider."""
        return self.observer_speed_slider.value

    @property
    def base_freq(self):
        """Return the current base frequency value from its slider."""
        return self.base_freq_slider.value

    def set_running(self, running):
        """Set whether the simulation is running or paused."""
        self.running = bool(running)

    def set_observed_frequency(self, freq):
        """Update the observed frequency shown in the readout box."""
        self.current_freq = float(freq)

    def consume_reset_request(self):
        """Return True once if a reset was requested, then clear the flag."""
        if self.reset_requested:
            self.reset_requested = False
            return True
        return False

    def handle_event(self, event):
        """Process window quit, button clicks, and slider input events."""
        if event.type == pygame.QUIT:
            self.should_quit = True
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.start_pause_rect.collidepoint(event.pos):
                self.running = not self.running
            elif self.reset_rect.collidepoint(event.pos):
                self.reset_requested = True
                self.running = False

        for slider in self.sliders:
            slider.handle_event(event)

    def draw(self, screen):
        """Draw the panel background, title image, sliders, readout, and buttons."""
        # Panel background and left border
        pygame.draw.rect(screen, self.palette["panel_bg"], self.panel_rect)
        pygame.draw.line(
            screen,
            self.palette["panel_border"],
            (self.panel_rect.x, self.panel_rect.y),
            (self.panel_rect.x, self.panel_rect.bottom),
            2,
        )

        # Main interface title
        title_rect = self.title_image.get_rect(
            midtop=(self.panel_rect.centerx, self.panel_rect.top + 12)
        )
        screen.blit(self.title_image, title_rect)
        
        # Sliders
        for slider in self.sliders:
            slider.draw(screen, self.font)

        # Live observed frequency readout
        pygame.draw.rect(
            screen, self.palette["readout_bg"], self.freq_box, border_radius=6
        )
        freq_surf = self.title_font.render(
            f"Observed frequency: {self.current_freq:.1f} Hz",
            True,
            self.palette["readout_text"],
        )
        screen.blit(freq_surf, freq_surf.get_rect(center=self.freq_box.center))

        # Start/Pause button at bottom
        
        button_image=self.pause_image if self.running else self.start_image
        screen.blit(button_image,button_image.get_rect(center=self.start_pause_rect.center),)
        screen.blit(self.reset_image,self.reset_image.get_rect(center=self.reset_rect.center),)
        
        # Reset button at bottom
        button_image=self.reset_image
        screen.blit(button_image,button_image.get_rect(center=self.reset_rect.center),)
        screen.blit(self.reset_image,self.reset_image.get_rect(center=self.reset_rect.center),)