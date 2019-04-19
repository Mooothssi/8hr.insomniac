class Scene():

    def __init__(self):
        self.ui_layer = None
        self.canvas_layer = None

    def load_layers(self):
        self.load_canvas()
        #self.load_hud()

    def load_canvas(self):
        pass


    def on_draw(self):
        self.ui_layer.draw()
        self.canvas_layer.draw()