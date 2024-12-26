import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw


class DrawingApp:
    """
    Класс для рисования на виртуальном холсте с возможностью выбора цвета, размера кисти
    и сохранения изображения в формате PNG.
    """
    def __init__(self, root):
        """
        Инициализация графического интерфейса рисовалки.
        :param root: корневое окно Tkinter
        """
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")
        # Создаем пустое изображение и инструмент для рисования
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)
        # Настраиваем холст
        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()
        # Инициализация других элементов интерфейса
        self.setup_ui()
        # Переменные для отслеживания координат мыши
        self.last_x, self.last_y = None, None

        self.pen_color = 'black'  # Цвет кисти по умолчанию
        self.previous_color = 'black'
        self.pen_size = 1  # Размер кисти по умолчанию

        # Подключение событий для рисования мышью
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.canvas.bind('<Button-3>', self.pick_color)
        self.erase_is_enable = False

    def setup_ui(self):
        """
        Настройка панели управления, включающей кнопки для очистки экрана, выбора цвета,
        сохранения изображения, а также выпадающий список для выбора размера кисти.
        """
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        # Кнопка "Очистить"
        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        # Кнопка "Выбрать цвет"
        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)
        # Унопка "Кисть"
        brush_button = tk.Button(control_frame, text="Кисть", command=self.use_paint)
        brush_button.pack(side=tk.LEFT)
        # Кнопка "Сохранить"
        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        # Выпадающий список для выбора размера кисти
        sizes = [1, 2, 5, 10, 20]  # Предопределенные размеры кисти
        self.pen_size_var = tk.IntVar(value=sizes[0])  # Переменная для хранения выбранного размера кисти
        size_menu = tk.OptionMenu(control_frame, self.pen_size_var, *sizes, command=self.update_pen_size)
        size_menu.pack(side=tk.LEFT)
        # Кнопка "Ластик"
        eraser_button = tk.Button(control_frame, text="Ластик", command=self.use_eraser)
        eraser_button.pack(side=tk.LEFT)

    def use_paint(self):
        self.erase_is_enable = False
        self.paint

    def use_eraser(self):
        """
        Включает режим "Ластик", который позволяет рисовать цветом фона.
        """
        # Сохраняем текущий цвет кисти
        if self.erase_is_enable == True:
            self.erase_is_enable = False
        else:
            self.previous_color = self.pen_color
        # Меняем цвет кисти на цвет фона (белый)
            self.pen_color = "white"
            self.erase_is_enable = True

    def paint(self, event):
        """
        Рисование на холсте при движении мыши.
        :param event: объект события, содержащий информацию о положении мыши
        """
        if self.erase_is_enable == False:
            self.pen_color = self.previous_color
        else:
            self.pen_color = "white"

        if self.last_x and self.last_y:
            # Рисуем на холсте линии со сглаживанием
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.pen_size, fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            # Рисуем линии на изображении, которое будет сохранено
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=self.pen_size)
        # Обновляем координаты последней точки
        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        """
        Сбрасывает координаты мыши после завершения рисования (отпускания кнопки мыши).
        :param event: объект события
        """
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        """
        Очищает холст и сбрасывает изображение в исходное пустое состояние.
        """
        self.canvas.delete("all")  # Удаляем все элементы с холста
        self.image = Image.new("RGB", (600, 400), "white")  # Удаляем все элементы с холста
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self):
        """
        Вызывает диалог для выбора цвета кисти. Обновляет текущий цвет кисти.
        """
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]
        self.previous_color = self.pen_color

    def save_image(self):
        """
        Сохраняет текущее изображение в файл формата PNG. Вызывает диалог выбора пути
        и уведомляет пользователя о завершении сохранения.
        """
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")

    def update_pen_size(self, size):
        """
        Обновляет размер кисти в соответствии с выбором пользователя в выпадающем списке.
        :param size: выбранный размер кисти
        """
        self.pen_size = int(size)  # Переменная pen_size обновляется в соответствии с выбором

    def pick_color(self, event):
        """
        Устанавливает текущим цветом для рисования цвет пикселя
        в текущих координатах при нажатии правай конопки мыши.
        :param event: объект события
        """
        rgb = self.image.getpixel((event.x, event.y))
        self.pen_color = '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])
        self.previous_color = self.pen_color


def main():
    """
    Запуск основного окна интерфейса приложения.
    """
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
