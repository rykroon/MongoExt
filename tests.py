from mongoext.fields import Field


if __name__ == '__main__':
    name = Field('name')
    a = name == 'A'
    b = name == 'B'
    c = name == 'C'
    d = name == 'D'

    a_and_b = a & b
    assert a_and_b == --a_and_b == {
        '$and': [
            {'name': {'$eq': 'A'}}, 
            {'name': {'$eq': 'B'}}
        ]
    }

    a_or_b = a | b
    assert a_or_b == --a_or_b == {
        '$or': [
            {'name': {'$eq': 'A'}}, 
            {'name': {'$eq': 'B'}}
        ]
    }

    c_and_d = c & d
    c_or_d = c | d

    assert a_and_b & c_and_d == --(a_and_b & c_and_d) == {
        '$and': [
            {'name': {'$eq': 'A'}}, 
            {'name': {'$eq': 'B'}},
            {'name': {'$eq': 'C'}}, 
            {'name': {'$eq': 'D'}}
        ]
    }

    assert a_and_b | c_and_d == --(a_and_b | c_and_d) =={
        '$or': [
            {'$and': [
                {'name': {'$eq': 'A'}}, 
                {'name': {'$eq': 'B'}}
        ]}, 
            {'$and': [
                {'name': {'$eq': 'C'}}, 
                {'name': {'$eq': 'D'}}
            ]}
        ]
    }

    assert a_or_b | c_or_d == --(a_or_b | c_or_d ) == {
        '$or': [
            {'name': {'$eq': 'A'}}, 
            {'name': {'$eq': 'B'}},
            {'name': {'$eq': 'C'}}, 
            {'name': {'$eq': 'D'}}
        ]
    }

    assert a_or_b & c_or_d == --(a_or_b & c_or_d ) == {
        '$and': [
            {'$or': [
                {'name': {'$eq': 'A'}}, 
                {'name': {'$eq': 'B'}}
        ]}, 
            {'$or': [
                {'name': {'$eq': 'C'}}, 
                {'name': {'$eq': 'D'}}
            ]}
        ]
    }

