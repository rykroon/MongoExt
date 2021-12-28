from dataclasses import is_dataclass, fields, asdict


def check_object(obj):
    if not hasattr(obj, '__dict__'):
        raise TypeError('Object must have a __dict__ attribute.')


def object_to_dict(obj):
    return {k: v for k, v in obj.__dict__.items() 
            if not k.startswith('_') or k == '_id'}


def check_dataclass(obj):
    if not is_dataclass(obj):
        raise TypeError('Object is not a dataclass.')

    if '_id' not in (f.name for f in fields(obj)):
        raise TypeError('Dataclass does not define an _id field.')


def dataclass_to_dict(obj):
    return asdict(obj)
