import pygame


class Slider:
    def __init__(
        self,
        label: str,
        rect: pygame.Rect,
        min_val: float,
        max_val: float,
        initial_val: float,
        unit: str = "",
    ):
        self.label = label
        self.rect = rect
        self.min_val = float(min_val)
        self.max_val = float(max_val)
        self.value = max(self.min_val, min(self.max_val, float(initial_val)))
        self.unit = unit
        self.dragging = False

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
        # Label + current numeric value
        text_surf = font.render(
            f"{self.label}: {self.value:.1f} {self.unit}".strip(),
            True,
            (235, 235, 240),
        )
        screen.blit(text_surf, (self.rect.x, self.rect.y - 20))

        # Track line
        pygame.draw.rect(screen, (90, 95, 110), self.rect, border_radius=4)

        # Filled portion + knob
        ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        knob_x = int(self.rect.x + ratio * self.rect.width)
        filled_rect = pygame.Rect(
            self.rect.x, self.rect.y, max(0, knob_x - self.rect.x), self.rect.height
        )
        pygame.draw.rect(screen, (70, 165, 250), filled_rect, border_radius=4)
        pygame.draw.circle(screen, (255, 255, 255), (knob_x, self.rect.centery), 8)


class Interface:
    def __init__(self, panel_rect: pygame.Rect, base_freq: float = 440.0):
        self.panel_rect = panel_rect
        self.font = pygame.font.SysFont("arial", 16)
        self.title_font = pygame.font.SysFont("arial", 18, bold=True)

        self.running = False
        self.reset_requested = False
        self.should_quit = False
        self.current_freq = float(base_freq)

        x = self.panel_rect.x + 16
        w = self.panel_rect.width - 32

        # Buttons: Start/Pause and Reset
        btn_w = (w - 10) // 2
        self.start_pause_rect = pygame.Rect(x, self.panel_rect.y + 52, btn_w, 34)
        self.reset_rect = pygame.Rect(x + btn_w + 10, self.panel_rect.y + 52, btn_w, 34)

        # Sliders (speeds in m/s, base frequency in Hz)
        # Keep max speed safely below speed of sound (343 m/s), e.g., 280 m/s
        self.source_speed_slider = Slider(
            "Source Speed", pygame.Rect(x, self.panel_rect.y + 135, w, 8), 0.0, 280.0, 50.0, "m/s"
        )
        self.observer_speed_slider = Slider(
            "Observer Speed", pygame.Rect(x, self.panel_rect.y + 195, w, 8), 0.0, 280.0, 0.0, "m/s"
        )
        self.base_freq_slider = Slider(
            "Base Freq (f0)", pygame.Rect(x, self.panel_rect.y + 255, w, 8), 100.0, 1200.0, base_freq, "Hz"
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
        # Side/bottom control panel background
        pygame.draw.rect(screen, (32, 35, 44), self.panel_rect)
        pygame.draw.line(
            screen,
            (65, 70, 85),
            (self.panel_rect.x, self.panel_rect.y),
            (self.panel_rect.x, self.panel_rect.bottom),
            2,
        )

        header = self.title_font.render("Controls & Readout", True, (245, 245, 250))
        screen.blit(header, (self.panel_rect.x + 16, self.panel_rect.y + 16))

        # Start/Pause button
        sp_color = (210, 140, 45) if self.running else (45, 165, 95)
        pygame.draw.rect(screen, sp_color, self.start_pause_rect, border_radius=6)
        sp_label = "Pause" if self.running else "Start"
        sp_text = self.font.render(sp_label, True, (255, 255, 255))
        screen.blit(sp_text, sp_text.get_rect(center=self.start_pause_rect.center))

        # Reset button
        pygame.draw.rect(screen, (75, 82, 100), self.reset_rect, border_radius=6)
        rst_text = self.font.render("Reset", True, (255, 255, 255))
        screen.blit(rst_text, rst_text.get_rect(center=self.reset_rect.center))

        # Sliders
        for slider in self.sliders:
            slider.draw(screen, self.font)

        # Live observed frequency readout
        freq_box = pygame.Rect(
            self.panel_rect.x + 16,
            self.panel_rect.y + 300,
            self.panel_rect.width - 32,
            44,
        )
        pygame.draw.rect(screen, (22, 24, 31), freq_box, border_radius=6)
        freq_surf = self.title_font.render(
            f"Observed: {self.current_freq:.1f} Hz", True, (110, 220, 175)
        )
        screen.blit(freq_surf, freq_surf.get_rect(center=freq_box.center))