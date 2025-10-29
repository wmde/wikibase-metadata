"""Sort Wikibase List"""

import enum
import strawberry


@strawberry.enum
class SortDirEnum(enum.Enum):
    """Sort Direction"""

    ASC = 0
    DESC = 1


@strawberry.enum
class SortColumnEnum(enum.Enum):
    """Sort Column"""

    TRIPLES = 0


@strawberry.input
class WikibaseSortInput:
    """Sort Wikibase List"""

    column: SortColumnEnum
    dir: SortDirEnum
