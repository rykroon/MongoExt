# MongoExt
A suite of utilities for increasing productivity with pymongo and motor.

```
In [1]: from pymongo import MongoClient

In [2]: from mongoext import CollectionExt

In [3]: client = MongoClient()

In [4]: db = client['test_db']

In [5]: coll = CollectionExt(name='test_collection', database=db)

In [6]: class Foo:
   ...:     ...
   ...:

In [7]: f = Foo()

In [8]: f.name = 'Alice'

In [9]: coll.insert_object(f)
Out[9]: <pymongo.results.InsertOneResult at 0x107766dc0>

In [10]: f._id
Out[10]: ObjectId('61b6c25592ac1c05b027bac9')

In [11]: f.name = 'Bob'

In [12]: coll.update_object(f)
Out[12]: <pymongo.results.UpdateResult at 0x10633f7c0>

In [13]: coll.get_by_id(f._id)
Out[13]: {'_id': ObjectId('61b6c25592ac1c05b027bac9'), 'name': 'Bob'}

In [14]: coll.delete_object(f)
Out[14]: <pymongo.results.DeleteResult at 0x107788400>

In [15]: coll.get_by_id(f._id) is None
Out[15]: True

```
