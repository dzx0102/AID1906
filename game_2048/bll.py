"""
    游戏逻辑控制器，负责处理游戏核心算法
"""
from model import DirectionModel
from model import Location
import random
class GameCoreController:
    def __init__(self):
        self.__list_merge = None
        self.__map = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.__list_empty_location = []
    @property
    def map(self):
        return self.__map
    def __zero_to_end(self):
        """
        将 0 移动到末尾
        :return:
        """
        for i in range(-1,-len(self.__list_merge) - 1,-1):
            if self.__list_merge[i] == 0:
                del self.__list_merge[i]
                self.__list_merge.append(0)
    def __merge(self):
        """
        先将中间的 0 元素移到末尾
        在合并相邻的相同元素
        :return:
        """
        self.__zero_to_end()
        for i in range(len(self.__list_merge) - 1):
            if self.__list_merge[i] == self.__list_merge[i + 1]:
                self.__list_merge[i] += self.__list_merge[i + 1]
                del self.__list_merge[i + 1]
                self.__list_merge.append(0)
    def __move_left(self):
        """
        将二维列表中的每行（从左到右）交给 __merge 实例方法进行操作
        :return:
        """
        for line in self.map:
            self.__list_merge = line
            self.__merge()
    def __move_right(self):
        """
        将二维列表中的每行（从右到左）交给 __merge 实例方法进行操作
        :return:
        """
        for line in self.map:
            self.__list_merge = line[::-1]
            self.__merge()
            line[::-1] = self.__list_merge
    def __move_up(self):
        self.__square_matrix_transpose()
        self.__move_left()
        self.__square_matrix_transpose()
    def __move_down(self):
        self.__square_matrix_transpose()
        self.__move_right()
        self.__square_matrix_transpose()
    def __square_matrix_transpose(self):
        for c in range(1, len(self.map)):
            for r in range(c, len(self.map)):
                self.map[r][c - 1], self.map[c - 1][r] = self.map[c - 1][r], self.map[r][c - 1]

    def move(self,dir):
        """
        移动
        :param dir: 方向，DirectionModel类型
        :return:
        """
        if dir == DirectionModel.UP:
            self.__move_up()
        elif dir == DirectionModel.DOWN:
            self.__move_down()
        elif dir == DirectionModel.LEFT:
            self.__move_left()
        elif dir == DirectionModel.RIGHT:
            self.__move_right()

    def generate_new_number(self):
        self.get_empty_location()
        if len(self.__list_empty_location) == 0:
            return
        # 随机选择一个位置生成新数字
        loc = random.choice(self.__list_empty_location)
        self.__map[loc.r_index][loc.c_index] = self.__select_random_number()
        # 因为在该位置生成了新数字，所以该位置就不是空位置了
        self.__list_empty_location.remove(loc)
    def __select_random_number(self):
        return 4 if random.randint(1, 10) == 1 else 2
    def get_empty_location(self):
        # 每次统计空位置，都先清空列表
        self.__list_empty_location.clear()
        # 获取所有空白位置
        for r in range(len(self.map)):
            for c in range(len(self.map[r])):
                if self.map[r][c] == 0:
                    self.__list_empty_location.append(Location(r, c))

    def is_game_over(self):
        """
        游戏是否结束
        :return: False表示没有结束，Ture表示结束
        """
        # 是否具有空位置
        if len(self.__list_empty_location) > 0:
            return False
        # 横向竖向没有相同元素
        for r in range(len(self.__map)):
            for c in range(len(self.__map[r]) - 1):
                if self.__map[r][c] == self.__map[r][c + 1] or self.__map[c][r] == self.__map[c + 1][r]:
                    return False
        return True

#------------------测试代码---------------------------
if __name__ == "__main__":
    controller = GameCoreController()
    # controller._GameCoreController__move_down()
    # print(controller.map)
    # controller.move(DirectionModel.UP)
    # print(controller.map)
    controller.generate_new_number()
    controller.generate_new_number()
    controller.generate_new_number()
    controller.generate_new_number()
    print(controller.map)