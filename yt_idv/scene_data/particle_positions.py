import numpy as np
import traitlets
from yt.data_objects.data_containers import YTDataContainer

from yt_idv.opengl_support import VertexArray, VertexAttribute
from yt_idv.scene_data.base_data import SceneData


class ParticlePositions(SceneData):
    name = "particle_positions"
    data_source = traitlets.Instance(YTDataContainer)
    particle_type = traitlets.Unicode("all")
    radius_field = traitlets.Unicode("particle_ones")
    color_field = traitlets.Unicode("particle_ones")
    size = traitlets.CInt(-1)

    @traitlets.default("vertex_array")
    def _default_vertex_array(self):
        va = VertexArray(name="particle_positions")
        positions = (
            self.data_source[self.particle_type, "particle_position"]
            .in_units("code_length")
            .astype("f4")
            .d
        )
        radii = self.data_source[self.particle_type, self.radius_field].astype("f4").d
        radii.shape = (radii.size, 1)
        color_field = (
            self.data_source[self.particle_type, self.color_field].astype("f4").d
        )
        color_field.shape = (color_field.size, 1)
        self.size = radii.size
        positions = np.concatenate(
            [positions, np.ones((self.size, 1), dtype="f4")], axis=1
        )
        va.attributes.append(VertexAttribute(name="model_vertex", data=positions))
        va.attributes.append(VertexAttribute(name="in_radius", data=radii))
        va.attributes.append(VertexAttribute(name="in_field_value", data=color_field))

        return va
