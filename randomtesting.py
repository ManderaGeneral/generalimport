from generalfile import Path

from generalimport import generalimport
generalimport("foobar")

import foobar.error as er

print(Path.__subclasses__())