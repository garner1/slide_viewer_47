import typing

from PyQt5 import QtGui
from PyQt5.QtCore import QRectF, QRect, Qt
from PyQt5.QtGui import QColor, QBrush

from PyQt5.QtWidgets import QGraphicsItem, QWidget

from elapsed_timer import elapsed_timer


class GraphicsGrid(QGraphicsItem):
    def __init__(self, grid_rects_0_level, color_alphas, bounding_rect, base_color_rgb=(0, 255, 0)):
        super().__init__()
        self.grid_rects_0_level = grid_rects_0_level
        self.color_alphas = color_alphas
        self.setAcceptedMouseButtons(Qt.NoButton)
        self.setAcceptHoverEvents(False)
        self.bounding_rect = bounding_rect
        self.base_color_rgb = base_color_rgb

        # self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        self.downsample = 1
        self.color_key__rects_0_level = {}

        from itertools import starmap
        self.star_map_ = starmap

        for grid_rect_0_level, color_alpha in zip(grid_rects_0_level, color_alphas):
            self.color_key__rects_0_level.setdefault(color_alpha, []).append(grid_rect_0_level)

        # self.color_rects = [[] for intensity in range(256)]
        # for grid_rect_0_level, intensity in zip(self.grid_rects_0_level, color_alphas):
        #     self.color_rects[intensity].append(grid_rect_0_level)

        self.recompute_bounding_rect()

    def recompute_bounding_rect(self):
        self.bounding_qrectf = QRectF(self.bounding_rect[0], self.bounding_rect[1],
                                      self.bounding_rect[2] / self.downsample,
                                      self.bounding_rect[3] / self.downsample)

    def update_downsmaple(self, downsample):
        self.downsample = downsample
        self.recompute_bounding_rect()

    def boundingRect(self):
        return self.bounding_qrectf

    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionGraphicsItem',
              widget: typing.Optional[QWidget] = ...):
        with elapsed_timer() as elapsed:
            painter.save()
            scale = 1 / self.downsample
            painter.scale(scale, scale)

            # for grid_rect, color in zip(self.grid_rects_0_level, self.color_alphas):
            #     painter.setBrush(color)
            #     painter.drawRect(*grid_rect)

            for color_alpha, rects in self.color_key__rects_0_level.items():
                color = QColor(*self.base_color_rgb, color_alpha)
                painter.setBrush(color)
                qrectfs = self.star_map_(QRectF, rects)
                painter.drawRects(qrectfs)

            # for color_key, grid_rects in enumerate(self.color_key__rects_0_level):
            #     if grid_rects:
            #         color = QColor(0, 255, 0, color_key)
            #         painter.setBrush(color)
            #         qrectfs = self.star_map_(QRectF, grid_rects)
            #         painter.drawRects(qrectfs)
            painter.restore()

            print("grid_paint ", elapsed())
