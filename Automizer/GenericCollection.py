from typing import TypeVar

from Automizer.DynaData import DynaData
from Automizer.PipelineData import PipelineData

S = TypeVar('S', bound=PipelineData)
D = TypeVar('D', bound=DynaData)
