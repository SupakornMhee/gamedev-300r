'''
World.py อันนี้เอาไว้สำหรับสร้างด่าน/โชว์ด่าน

World.py ต้องมี Attribute อะไรบ้าง
1. Background สำหรับ Display
2. Player -- ซึ่งมาจาก EntityBase อีกที
3. Enemies -- ซึ่งมาจาก EntityBase อีกที
4. List of Enemies -- ซึ่งเป็น List ของ Enemies อีกทีนึง

ใน EntityBase มีอะไร
1. direction -- Up Down Left Right
2. animation_list -- 

World.py ต้องมี Function อะไรบ้าง

'''


class World:
    def __init__(self):
        pass

    def update(self, dt, events):
        pass

    def render(self):
        pass
