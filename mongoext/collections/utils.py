from dataclasses import is_dataclass, fields, asdict


def check_object(obj):
    if not hasattr(obj, '__dict__') and not hasattr(obj, '__slots__'):
        raise TypeError('Object must have a __dict__ or __slots__ attribute.')

    if hasattr(obj, '__slots__'):
        if '_id' not in obj.__slots__:
            raise TypeError('Slot instance does not define an _id field.')


def object_to_dict(obj):
    if hasattr(obj, '__slots__'):
        return {k: getattr(obj, k, None) for k in obj.__slots__ if not k.startswith('_') or k == '_id'}
    
    return {k: v for k, v in vars(obj).items() if not k.startswith('_') or k == '_id'}


def check_dataclass(obj):
    if not is_dataclass(obj):
        raise TypeError('Object is not a dataclass.')

    if '_id' not in (f.name for f in fields(obj)):
        raise TypeError('Dataclass does not define an _id field.')


def dataclass_to_dict(obj):
    return asdict(obj)

