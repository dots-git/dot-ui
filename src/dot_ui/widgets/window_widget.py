from .container_widget import *


class Window(Container):
    def __init__(
        self, *args, width=1000, height=600, title="New Window", icon=None, fullscreen=False, **kwargs
    ):
        Container.__init__(self, *args, x=0, y=0, width=width, height=height, **kwargs)
        self.transform.jump()
        if icon == None:
            icon = UI_MODULE_PATH + "/data/icon.png"

        self.width = width
        self.height = height
        self.title = title
        self.icon = icon

        self._min_delta = 1 / 60
        self.fps_update_interval = 0.5
        self.print_fps = False

        self._close = False

        self._initialized = False

        self._fullscreen = fullscreen

    def initialize(self):
        pygame.init()
        pygame.mixer.init()  ## For sound
        pygame.font.init()

        Input.init()

        self._init()

        self.screen = None
        if self._fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(
                (self.width, self.height), pygame.RESIZABLE
            )
        pygame.display.set_caption(self.title, self.icon)
        pygame.display.set_icon(pygame.image.load(self.icon))

        current_time = time.time()
        self.time_last_frame = current_time
        self.delta = self._min_delta
        self.delta_list = []
        self.fps_display_update_time = self.fps_update_interval
        self._initialized = True

    def open(self):
        if not self._initialized:
            self.initialize()
        while True:
            self.size = pygame.display.get_surface().get_size()
            self.size.jump()

            Timer.autoprint = True


            Input.tick()

            
            events = pygame.event.get()

            for event in events:
                # gets all the events which have occured till now and keeps tab of them.
                # listening for the the X button at the top
                Input.events(event)
                if event.type == pygame.QUIT:
                    self._close = True
                self._events(event)

            self._tick(self.delta)

            Widget.renderer.tick()

            Widget.renderer.render(self, self.delta)

            pygame.display.get_surface().blit(self.surface, (0, 0))

            pygame.display.flip()

            current_time = time.time()
            self.delta = current_time - self.time_last_frame
            if self.delta < self._min_delta:
                time.sleep(self._min_delta - self.delta)
                current_time = time.time()
                self.delta = current_time - self.time_last_frame
            self.time_last_frame = current_time

            if self.print_fps:

                if self.delta == 0:
                    self.delta += 10e-255
                self.delta_list.append(self.delta)
                self.fps_display_update_time -= self.delta

                if self.fps_display_update_time < 0:
                    print(
                        "Fps: %i (Min: %i, Max: %i)"
                        % (
                            round(len(self.delta_list) / sum(self.delta_list)),
                            round(1 / max(self.delta_list)),
                            round(1 / min(self.delta_list)),
                        )
                    )
                    self.curr_fps = 1 / self.delta
                    self.delta_list = []
                    self.fps_display_update_time = self.fps_update_interval

            if self._close:
                pygame.quit()
                return

    def close(self):
        self._close = True

    @property
    def fps(self):
        return int(1 / self.delta)

    @property
    def max_fps(self):
        return int(1 / self._min_delta)

    @max_fps.setter
    def max_fps(self, value):
        self._min_delta = 1 / value

    @property
    def fullscreen(self):
        return self._fullscreen

    @fullscreen.setter
    def fullscreen(self, value):

        if self._fullscreen != value and self._initialized:
            if value:
                self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            else:
                self.screen = pygame.display.set_mode(
                    (self.width, self.height), pygame.RESIZABLE
                )

        self._fullscreen = value
