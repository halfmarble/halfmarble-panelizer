# Copyright 2021 HalfMarble LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

# See the License for the specific language governing permissions and
# limitations under the License.

import math
import os

from kivy.graphics import Line, ClearBuffers, ClearColor
from Constants import *
from PcbFile import generate_mouse_bite_gm1_files
from Utilities import load_image, rmrf, colored_mask
import tempfile


class AppSettings:

    def __init__(self):
        self._gap = 0
        self._top = 0
        self._bottom = 0
        self._bite = 0
        self._bite_hole_radius = 1
        self._bite_hole_space = 3
        self._bites_count_x = 0
        self._bites_count_y = 0
        self._bites_image = None

        self._tmp_folder = tempfile.TemporaryDirectory().name
        try:
            os.mkdir(self._tmp_folder)
        except FileExistsError:
            pass

        self.reset()

    def reset(self):
        self._top = PCB_PANEL_TOP_RAIL_MM
        self._bottom = PCB_PANEL_BOTTOM_RAIL_MM
        self._gap = PCB_PANEL_GAP_MM
        self._bite = PCB_PANEL_BITES_SIZE_MM
        self._bites_count_x = PCB_PANEL_BITES_COUNT_X
        self._bites_count_y = PCB_PANEL_BITES_COUNT_Y
        self._bites_image = None

    @property
    def top(self):
        return self._top

    @property
    def bottom(self):
        return self._bottom

    @property
    def gap(self):
        return self._gap

    @property
    def bite(self):
        return self._bite

    @property
    def bites_count_x(self):
        return self._bites_count_x

    @property
    def bites_count_y(self):
        return self._bites_count_y

    @property
    def bite_hole_radius(self):
        return self._bite_hole_radius

    @property
    def bite_hole_space(self):
        return self._bite_hole_space

    @property
    def bites_image(self):
        if self._bites_image is None and self._tmp_folder is not None:
            generate_mouse_bite_gm1_files(self._tmp_folder,
                                          origin=(0, 0), size=(self._bite, self._gap), arc=1, close=True)
            self._bites_image = load_image(self._tmp_folder, 'edge_cuts_mask.png')
            if self._bites_image is not None:
                self._bites_image = colored_mask(self._bites_image, Color(1, 1, 1, 1))
        return self._bites_image

    def cleanup(self):
        rmrf(self._tmp_folder)


AppSettings = AppSettings()
