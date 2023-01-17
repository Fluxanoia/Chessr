from src.engine.factory import Factory
from src.game.sprite import ChessrSprite, GroupType
from src.utils.helpers import FloatVector


class CoordinateText(ChessrSprite):

    def __init__(
        self,
        text : str,
        xy : FloatVector,
        scale : float
    ):
        font = Factory.get().file_manager.load_default_font(int(8 * scale))
        image = font.render(text, True, (255, 255, 255))
        super().__init__(xy, GroupType.UI, image, scale = scale)

    def _calculate_position(self, xy : FloatVector) -> FloatVector:
        if self.rect is None:
            return xy
        x, y = xy
        w, h = self.rect.size
        return (x - w / 2, y - h / 2)
