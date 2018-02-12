from collections import UserDict

class QuestionState(UserDict) :
    def __init__(self, *args, **kwargs):
        super(QuestionState, self).__init__(*args, **kwargs)
        self.__dict__ = self
        
    