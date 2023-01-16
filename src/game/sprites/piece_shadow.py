from src.engine.factory import Factory
from src.game.sprite import ChessrSprite, GroupType
from src.utils.enums import ShadowType
from src.utils.helpers import FloatVector


class PieceShadow(ChessrSprite):

    def __init__(self, xy : FloatVector, scale : float) -> None:
        self.__type = ShadowType.DARK

        spritesheet = Factory.get().board_spritesheet
        image_src_rect = spritesheet.get_shadow_srcrect(self.__type, scale)
        image = spritesheet.get_image(image_src_rect, scale)

        super().__init__(xy, GroupType.SHADOW, image, scale = scale)

    def calculate_position(self, xy : FloatVector) -> FloatVector:
        rect_height = self.rect.h if not self.rect is None else 0
        return (xy[0], xy[1] - rect_height - 2 * self.scale)

    def set_alpha(self, alpha : int) -> None:
        if self.image is None:
            return
        self.image.set_alpha(alpha)
