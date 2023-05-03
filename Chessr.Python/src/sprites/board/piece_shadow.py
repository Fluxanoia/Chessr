from src.engine.factory import Factory
from src.engine.group_manager import DrawingPriority, GroupType
from src.engine.spritesheets.shadow_spritesheet import ShadowType
from src.sprites.sprite import ChessrSprite
from src.utils.enums import Anchor
from src.utils.helpers import FloatVector


class PieceShadow(ChessrSprite):

    def __init__(self, xy : FloatVector, scale : float) -> None:
        self.__type = ShadowType.DARK

        spritesheet = Factory.get().shadow_spritesheet
        image_src_rect = spritesheet.get_src_rect(self.__type, scale)
        image = spritesheet.get_image(image_src_rect, scale)

        self.__scale = scale

        super().__init__(
            xy,
            GroupType.GAME_PIECE,
            DrawingPriority.MINUS_ONE,
            image,
            anchor=Anchor.BOTTOM_LEFT)

    def _calculate_position(self, xy : FloatVector) -> FloatVector:
        x, y = xy
        return super()._calculate_position((x, y - 2 * self.__scale))

    def set_alpha(self, alpha : int) -> None:
        if self.image is None:
            return
        self.image.set_alpha(alpha)
