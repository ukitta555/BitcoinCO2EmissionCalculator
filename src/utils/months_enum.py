import enum


class StrEnum(str, enum.Enum):
    pass


class MonthEnum(StrEnum):
    JANUARY = 'Jan'
    FEBRUARY = 'Feb'
    MARCH = 'Mar'
    APRIL = 'Apr'
    MAY = 'May'
    JUNE = 'Jun'
    JULY = 'Jul'
    AUGUST = 'Aug'
    SEPTEMBER = 'Sep'
    OCTOBER = 'Oct'
    NOVEMBER = 'Nov'
    DECEMBER = 'Dec'

    @staticmethod
    def as_list():
        return list(map(lambda x: x.value, dict(MonthEnum.__members__).values()))

