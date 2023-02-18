from src.engine.factory import Factory
from src.game.sprite import ChessrSprite, GroupType
from src.utils.enums import Anchor, ShadowType
from src.utils.helpers import FloatVector


class PieceShadow(ChessrSprite):

    def __init__(self, xy : FloatVector, scale : float) -> None:
        self.__type = ShadowType.DARK

        spritesheet = Factory.get().board_spritesheet
        image_src_rect = spritesheet.get_shadow_srcrect(self.__type, scale)
        image = spritesheet.get_image(image_src_rect, scale)

        super().__init__(xy, GroupType.SHADOW, image, scale=scale, anchor=Anchor.BOTTOM_LEFT)

    def _calculate_position(self, xy : FloatVector) -> FloatVector:
        x, y = xy
        return super()._calculate_position((x, y - 2 * self.scale))

    def delete(self) -> None:
        if not self.group is None:
            Factory.get().group_manager.get_group(self.group).remove(self)

    def set_alpha(self, alpha : int) -> None:
        if self.image is None:
            return
        self.image.set_alpha(alpha)
