
class Rerun:
    
    def __init__(self,repeat_num:int) -> None:
        self.repeat_num = repeat_num
    
    def set_repeat_num(self,repeat_num):
        self.repeat_num = repeat_num

    def start(self, *functions):
        for _ in range(self.repeat_num):
            for fun in functions:
                fun()