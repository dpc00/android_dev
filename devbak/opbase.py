
class OpBase():
    def __init__(self, *args):
        kt = ('npl1', 'npl2', 'opts')
        for k, v in zip(kt, args):
            setattr(self, k, v)
