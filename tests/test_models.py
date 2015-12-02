#! -*- coding: utf-8 -*-

from app.models import Activity

def test_activity():
    data = dict(
        id=1,
        type="free",
        name=u"第一个活动",
        name_en="First Activity",
    )
    obj = Activity.objects.create(**data)
    print obj

if __name__ == "__main__":
    test_activity()