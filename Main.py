import tkinter as tk
from tkinter import ttk
import time
import threading

class ElevatorLogic:
    def __init__(self, total_floors, elevator_id):
        self.elevator_id = elevator_id  # 电梯编号 1/2
        self.total_floors = total_floors
        self.current_floor = 1
        self.direction = 1  # 1上行 -1下行
        self.targets = set()
        self.is_running = False
        self.gui_callback = None
        self.root = None

    def set_gui(self, callback, root):
        self.gui_callback = callback
        self.root = root

    def request_floor(self, floor):
        #楼层请求
        if 1 <= floor <= self.total_floors:
            self.targets.add(floor)
            if not self.is_running:
                self.is_running = True
                threading.Thread(target=self.run, daemon=True).start()

    def run(self):
        #主循环算法
        while self.targets:
            # 筛选当前方向的目标
            if self.direction == 1:
                current_targets = [f for f in self.targets if f >= self.current_floor]
            else:
                current_targets = [f for f in self.targets if f <= self.current_floor]

            # 无目标则换向
            if not current_targets:
                self.direction *= -1
                continue

            # 排序目标
            current_targets.sort(reverse=(self.direction == -1))
            for target in current_targets:
                self.move_to(target)

        self.is_running = False
        self.update_gui()

    def move_to(self, target_floor):
        #移动到目标楼层
        while self.current_floor != target_floor:
            time.sleep(0.5)
            self.current_floor += self.direction
            self.update_gui()

        # 到达楼层，移除请求
        if target_floor in self.targets:
            self.targets.remove(target_floor)
        self.update_gui()
        time.sleep(0.8)

    def update_gui(self):
        #刷新界面
        if self.gui_callback and self.root:
            self.root.after(0, self.gui_callback)

class DoubleElevatorApp:
    def __init__(self, root, total_floors=10):
        self.root = root
        self.root.title("双电梯 LOOK 算法并行模拟器")
        self.total_floors = total_floors

        # 配色方案（双电梯区分）
        self.color_shaft = "#f8f9fa"
        self.color_car1 = "#2d8bfd"  # 电梯1：蓝色
        self.color_car2 = "#198754"  # 电梯2：绿色
        self.color_btn_active = "#ffc107"
        self.color_btn_normal = "#e9ecef"

        # 初始化两部独立电梯
        self.elevator1 = ElevatorLogic(total_floors, 1)
        self.elevator2 = ElevatorLogic(total_floors, 2)
        self.elevator1.set_gui(self.refresh_all, self.root)
        self.elevator2.set_gui(self.refresh_all, self.root)

        # 按钮存储
        self.buttons = {}
        self.setup_ui()

    def setup_ui(self):
        """构建界面布局"""
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack()

        # ========== 左侧：双电梯井道 ==========
        elevator_frame = ttk.Frame(main_frame)
        elevator_frame.grid(row=0, column=0, padx=20)

        # 电梯1 井道
        shaft1 = ttk.LabelFrame(elevator_frame, text="电梯 1", padding=10)
        shaft1.grid(row=0, column=0, padx=10)
        # 电梯2 井道
        shaft2 = ttk.LabelFrame(elevator_frame, text="电梯 2", padding=10)
        shaft2.grid(row=0, column=1, padx=10)

        # 画布参数
        self.canvas_h = 500
        self.canvas_w = 120
        self.floor_h = self.canvas_h // self.total_floors

        # 创建两个画布
        self.canvas1 = self.create_shaft(shaft1)
        self.canvas2 = self.create_shaft(shaft2)

        # 绘制电梯轿厢
        self.car1 = self.create_car(self.canvas1, self.color_car1)
        self.car2 = self.create_car(self.canvas2, self.color_car2)

        # ========== 右侧：楼层控制面板 ==========
        ctrl_frame = ttk.LabelFrame(main_frame, text="楼层呼叫面板", padding=15)
        ctrl_frame.grid(row=0, column=1, sticky="n")

        # 从上到下生成楼层按钮
        for floor in range(self.total_floors, 0, -1):
            row = ttk.Frame(ctrl_frame)
            row.pack(pady=4, fill="x")
            ttk.Label(row, text=f"{floor}F", width=4, font=("黑体", 10)).pack(side="left")

            # 上行按钮
            if floor < self.total_floors:
                btn = tk.Button(row, text="▲", width=4, bg=self.color_btn_normal,
                               command=lambda f=floor: self.call_elevator(f, "up"))
                btn.pack(side="left", padx=3)
                self.buttons[(floor, "up")] = btn
            # 下行按钮
            if floor > 1:
                btn = tk.Button(row, text="▼", width=4, bg=self.color_btn_normal,
                               command=lambda f=floor: self.call_elevator(f, "down"))
                btn.pack(side="left", padx=3)
                self.buttons[(floor, "down")] = btn

        # ========== 底部：双状态显示 (已修复：替换为tk.Label，支持height) ==========
        self.status_var = tk.StringVar()
        # 修复点：ttk.Label 不支持 height，改用 tk.Label
        status_bar = tk.Label(main_frame, textvariable=self.status_var, relief="sunken",
                               height=2, font=("黑体", 10))
        status_bar.grid(row=1, column=0, columnspan=2, pady=15, sticky="ew")
        self.refresh_all()

    def create_shaft(self, parent):
        #创建电梯井道画布
        canvas = tk.Canvas(parent, width=self.canvas_w, height=self.canvas_h,
                          bg=self.color_shaft, bd=2, relief="sunken")
        canvas.pack()
        # 绘制楼层线
        for i in range(self.total_floors):
            y = i * self.floor_h
            canvas.create_line(0, y, self.canvas_w, y, fill="#ced4da")
            floor_num = self.total_floors - i
            canvas.create_text(12, y + self.floor_h/2, text=str(floor_num),
                               font=("Arial", 10, "bold"), anchor="w")
        return canvas

    def create_car(self, canvas, color):
        #创建电梯轿厢
        y = self.get_car_y(1)
        return canvas.create_rectangle(30, y, self.canvas_w-10, y+self.floor_h-5,
                                       fill=color, outline="#212529", width=2)

    def get_car_y(self, floor):
        #计算轿厢坐标
        return (self.total_floors - floor) * self.floor_h

    def get_best_elevator(self, target_floor):
        #调度
        e1 = self.elevator1
        e2 = self.elevator2

        dist1 = abs(e1.current_floor - target_floor)
        dist2 = abs(e2.current_floor - target_floor)

        # 顺路优先
        e1_good = (e1.direction == 1 and target_floor >= e1.current_floor) or \
                  (e1.direction == -1 and target_floor <= e1.current_floor)
        e2_good = (e2.direction == 1 and target_floor >= e2.current_floor) or \
                  (e2.direction == -1 and target_floor <= e2.current_floor)

        if e1_good and not e2_good:
            return e1
        if e2_good and not e1_good:
            return e2
        #选距离近的
        return e1 if dist1 <= dist2 else e2

    def call_elevator(self, floor, direction):
        best_e = self.get_best_elevator(floor)
        best_e.request_floor(floor)
        # 按钮高亮
        btn = self.buttons.get((floor, direction))
        if btn:
            btn.config(bg=self.color_btn_active, state="disabled")

    def refresh_all(self):
        # 移动电梯1
        y1 = self.get_car_y(self.elevator1.current_floor)
        self.canvas1.coords(self.car1, 30, y1, self.canvas_w-10, y1+self.floor_h-5)
        # 移动电梯2
        y2 = self.get_car_y(self.elevator2.current_floor)
        self.canvas2.coords(self.car2, 30, y2, self.canvas_w-10, y2+self.floor_h-5)

        # 重置
        for (f, d), btn in self.buttons.items():
            if f not in self.elevator1.targets and f not in self.elevator2.targets:
                btn.config(bg=self.color_btn_normal, state="normal")

        # 更新状态
        def get_status(e):
            dir_str = "上行" if e.direction == 1 else "下行"
            state = dir_str if e.is_running else "待机"
            return f"电梯{e.elevator_id}：{e.current_floor}F | {state} | 队列{sorted(list(e.targets))}"

        self.status_var.set(f"{get_status(self.elevator1)}\n{get_status(self.elevator2)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DoubleElevatorApp(root, total_floors=10)
    root.mainloop()