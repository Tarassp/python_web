class Meta(type):
    children_number = 0
    
    @classmethod
    def __prepare__(mcs, name, bases):
        dct = {'class_number' : Meta.children_number}
        Meta.children_number += 1
        return dct
    
    # Alternative approach
    # def __new__(mcl, name, bases, namespace, **kwargs):
    #     namespace['class_number'] = Meta.children_number
    #     Meta.children_number += 1
    #     return super().__new__(mcl, name, bases, namespace, **kwargs)
    
    
    
Meta.children_number = 0

class Cls1(metaclass=Meta):
    def __init__(self, data):
        self.data = data


class Cls2(metaclass=Meta):
    def __init__(self, data):
        self.data = data
        
        
def main():
    assert (Cls1.class_number, Cls2.class_number) == (0, 1)
    a, b = Cls1(''), Cls2('')
    assert (a.class_number, b.class_number) == (0, 1)
    


if __name__ == '__main__':
    main()
    
