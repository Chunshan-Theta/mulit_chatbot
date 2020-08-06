from MongoDbTool.common import MongoBasicClient


class TravelUnit(dict):
    def __init__(self, owner, title):
        super().__init__()
        self.__setitem__("owner", owner)
        self.__setitem__("title", title)
        self.__setitem__("units", [])

    def new_unit(self, shortcode):
        self.__getitem__("units").append({
            "shortcode": shortcode
        })

    def add_unit(self,unit):
        self.__getitem__("units").append(unit)

    @classmethod
    def is_units(cls, tu) -> bool:
        if 'owner' not in tu: return False
        if 'title' not in tu: return False
        if 'units' not in tu: return False
        if isinstance(list, type(tu["units"])): return False
        for unit in tu["units"]:
            if "shortcode" not in unit:
                return False
        return True

    @classmethod
    def from_dict(cls, obj):
        assert cls.is_units(obj), "invalid format"
        owner = obj['owner']
        title = obj['title']
        tu_temp = TravelUnit(owner,title)
        for unit in obj['units']:
            tu_temp.add_unit(unit)
        return tu_temp


def new_travel_unit(tu: TravelUnit):
    with MongoBasicClient(host="cluster0.enocw.mongodb.net", db_name="travelHunt", db_list_name="unit") as db_client:
        db_client.insert(val=tu)


def add_unit_travel_units(travel_units_uuid: str, shortcode: str):
    with MongoBasicClient(host="cluster0.enocw.mongodb.net", db_name="travelHunt", db_list_name="unit") as db_client:
        obj = db_client.query(uuid=travel_units_uuid, limit=1)[0]

        obj = TravelUnit.from_dict(dict(obj))
        obj.new_unit(shortcode=shortcode)
        db_client.update(filters={"uuid": travel_units_uuid}, **obj)