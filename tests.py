from mongoext.fields import Field


if __name__ == '__main__':
    foo = Field('foo')
    a = foo == 'A'
    b = foo == 'B'
    c = foo == 'C'
    d = foo == 'D'

    anb = a & b
    assert anb == --anb == {
        '$and': [
            {'foo': {'$eq': 'A'}}, 
            {'foo': {'$eq': 'B'}}
        ]
    }

    aob = a | b
    assert aob == --aob == {
        '$or': [
            {'foo': {'$eq': 'A'}}, 
            {'foo': {'$eq': 'B'}}
        ]
    }

    cnd = c & d
    cod = c | d

    assert anb & cnd == --(anb & cnd) == {
        '$and': [
            {'foo': {'$eq': 'A'}}, 
            {'foo': {'$eq': 'B'}},
            {'foo': {'$eq': 'C'}}, 
            {'foo': {'$eq': 'D'}}
        ]
    }

    assert anb | cnd == --(anb | cnd) =={
        '$or': [
            {'$and': [
                {'foo': {'$eq': 'A'}}, 
                {'foo': {'$eq': 'B'}}
        ]}, 
            {'$and': [
                {'foo': {'$eq': 'C'}}, 
                {'foo': {'$eq': 'D'}}
            ]}
        ]
    }

    assert aob | cod == --(aob | cod ) == {
        '$or': [
            {'foo': {'$eq': 'A'}}, 
            {'foo': {'$eq': 'B'}},
            {'foo': {'$eq': 'C'}}, 
            {'foo': {'$eq': 'D'}}
        ]
    }

    assert aob & cod == --(aob & cod ) == {
        '$and': [
            {'$or': [
                {'foo': {'$eq': 'A'}}, 
                {'foo': {'$eq': 'B'}}
        ]}, 
            {'$or': [
                {'foo': {'$eq': 'C'}}, 
                {'foo': {'$eq': 'D'}}
            ]}
        ]
    }

