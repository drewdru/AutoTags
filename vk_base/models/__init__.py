import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

from . import albums_tags
from . import albums
from . import images_tags
from . import images
from . import tags

from . import modelsHelper

modelsHelper.Base.metadata.create_all(modelsHelper.engine)
