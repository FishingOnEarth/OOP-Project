import pygame

#can manually change here
BACKGROUND_COLOR = (24, 27, 36)

COLOR_PALETTE = {
    "panel_bg": (32, 35, 44),
    "panel_border": (65, 70, 85),
    "title_text": (245, 245, 250),
    "label_text": (235, 235, 240),
    "slider_track": (90, 95, 110),
    "slider_fill": (70, 165, 250),
    "slider_knob": (255, 255, 255),
    "start_btn": (45, 165, 95),
    "pause_btn": (210, 140, 45),
    "reset_btn": (75, 82, 100),
    "btn_text": (255, 255, 255),
    "readout_bg": (22, 24, 31),
    "readout_text": (110, 220, 175),
}

class Slider:
    def __init__(
        self,
        label: str,
        rect: pygame.Rect,
        min_val: float,
        max_val: float,
        initial_val: float,
        unit: str = "",
        palette: dict[str, tuple[int, int, int]] | None = None
    ):
        self.label = label
        self.rect = rect
        self.min_val = float(min_val)
        self.max_val = float(max_val)
        self.value = max(self.min_val, min(self.max_val, float(initial_val)))
        self.unit = unit
        self.dragging = False
        self.palette = palette if palette is not None else COLOR_PALETTE

    def _set_from_x(self, x: int):
        if self.rect.width <= 0:
            return
        ratio = (x - self.rect.x) / self.rect.width
        ratio = max(0.0, min(1.0, ratio))
        self.value = self.min_val + ratio * (self.max_val - self.min_val)

    def handle_event(self, event: pygame.event.Event):
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

    def draw(self, screen: pygame.Surface, font: pygame.font.Font):
        text_surf = font.render(
            f"{self.label}: {self.value:.1f} {self.unit}".strip(),
            True,
            self.palette["label_text"],
        )
        screen.blit(text_surf, (self.rect.x, self.rect.y - 20))

        pygame.draw.rect(
            screen, self.palette["slider_track"], self.rect, border_radius=4
        )

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
    def __init__(self, panel_rect: pygame.Rect, base_freq: float = 440.0,
                 bg_color: tuple[int, int,int] = BACKGROUND_COLOR, 
                 palette: dict[str, tuple[int, int, int]]|None = None):
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
        btn_h = 36
        bottom_margin = 16

        # Buttons: Start/Pause and Reset
        btn_y = self.panel_rect.bottom - bottom_margin - btn_h
        self.freq_box = pygame.Rect(x, btn_y - 58, w, 44)
        self.reset_rect = pygame.Rect(x + btn_w + 10, btn_y, btn_w, btn_h)

        # Sliders (speeds in m/s, base frequency in Hz)
        # Keep max speed safely below speed of sound (343 m/s), e.g., 280 m/s
        self.source_speed_slider = Slider(
            "Source Speed", pygame.Rect(x, self.panel_rect.y + 85, w, 8), 
            0.0, 280.0, 50.0, "m/s", palette=self.palette
        )
        self.observer_speed_slider = Slider(
            "Observer Speed", pygame.Rect(x, self.panel_rect.y + 195, w, 8), 
            0.0, 280.0, 0.0, "m/s", palette=self.palette
        )
        self.base_freq_slider = Slider(
            "Base Freq (f0)", pygame.Rect(x, self.panel_rect.y + 255, w, 8), 
            100.0, 1200.0, base_freq, "Hz", palette=self.palette
        )
        self.sliders = [
            self.source_speed_slider,
            self.observer_speed_slider,
            self.base_freq_slider,
        ]

    @property
    def source_speed(self):
        return self.source_speed_slider.value

    @property
    def observer_speed(self):
        return self.observer_speed_slider.value

    @property
    def base_freq(self):
        return self.base_freq_slider.value

    def set_running(self, running: bool):
        self.running = bool(running)

    def set_observed_frequency(self, freq: float):
        self.current_freq = float(freq)

    def consume_reset_request(self):
        if self.reset_requested:
            self.reset_requested = False
            return True
        return False

    def handle_event(self, event: pygame.event.Event):
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

    def draw(self, screen: pygame.Surface):
        # Panel background and left border
        pygame.draw.rect(screen, self.palette["panel_bg"], self.panel_rect)
        pygame.draw.line(
            screen,
            self.palette["panel_border"],
            (self.panel_rect.x, self.panel_rect.y),
            (self.panel_rect.x, self.panel_rect.bottom),
            2,
        )

        # Main interface title (2d doppler)
        title_surf = self.title_font.render(
            "2D doppler visualization", True, self.palette["title_text"]
        )
        screen.blit(title_surf, (self.panel_rect.x + 16, self.panel_rect.y + 18))

        # Sliders
        for slider in self.sliders:
            slider.draw(screen, self.font)

        # Live observed frequency readout
        pygame.draw.rect(
            screen, self.palette["readout_bg"], self.freq_box, border_radius=6
        )
        freq_surf = self.title_font.render(
            f"Observed: {self.current_freq:.1f} Hz",
            True,
            self.palette["readout_text"],
        )
        screen.blit(freq_surf, freq_surf.get_rect(center=self.freq_box.center))

        # Start/Pause button at bottom
        sp_color = (
            self.palette["pause_btn"] if self.running else self.palette["start_btn"]
        )
        pygame.draw.rect(screen, sp_color, self.start_pause_rect, border_radius=6)
        sp_label = "Pause" if self.running else "Start"
        sp_text = self.font.render(sp_label, True, self.palette["btn_text"])
        screen.blit(sp_text, sp_text.get_rect(center=self.start_pause_rect.center))

        # Reset button at bottom
        pygame.draw.rect(
            screen, self.palette["reset_btn"], self.reset_rect, border_radius=6
        )
        rst_text = self.font.render("Reset", True, self.palette["btn_text"])
        screen.blit(rst_text, rst_text.get_rect(center=self.reset_rect.center))