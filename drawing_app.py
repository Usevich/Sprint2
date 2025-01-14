import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, simpledialog
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
        self.canvas_color = 'white'
        self.canvas = tk.Canvas(root, width=600, height=400, bg=self.canvas_color)
        self.canvas.pack()
        # Инициализация других элементов интерфейса

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
        self.register_shortcuts()
        self.setup_ui()

    def register_shortcuts(self):
        """
        Регистрация горячих клавиш для быстрого доступа к функциям интерфейса.
        """
        self.root.bind('<Control-s>', self.save_image)  # Ctrl+S для сохранения изображения
        self.root.bind('<Control-c>', self.choose_color)  # Ctrl+C для выбора цвета

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
        # Холст для предварительного просмотра цвета кисти
        self.preview_canvas = tk.Canvas(control_frame, width=20, height=20, bg=self.pen_color)
        self.preview_canvas.pack(side=tk.LEFT)
        # Кнопка для изменения размера холста
        change_size_button = tk.Button(control_frame, text="Изменить размер холста", command=self.change_canvas_size)
        change_size_button.pack(side=tk.LEFT)
        # Кнопка "Текст"
        text_button = tk.Button(control_frame, text="Текст", command=self.add_text)
        text_button.pack(side=tk.LEFT)
        # Кнопка "Изменить фон"
        bg_color_button = tk.Button(control_frame, text="Изменить фон", command=self.change_background_color)
        bg_color_button.pack(side=tk.LEFT)

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
            self.erase_is_enable = True

    def paint(self, event):
        """
        Рисование на холсте при движении мыши.
        :param event: объект события, содержащий информацию о положении мыши
        """
        if self.erase_is_enable == False:
            self.pen_color = self.previous_color
        else:
            self.pen_color = self.canvas_color

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

    def choose_color(self, event=None):
        """
        Вызывает диалог для выбора цвета кисти. Обновляет текущий цвет кисти.
        """
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]
        self.previous_color = self.pen_color
        # Обновляем цвет холста предварительного просмотра
        self.preview_canvas.config(bg=self.pen_color)

    def save_image(self, event=None):
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

    def change_canvas_size(self):
        """
        Изменяет размер холста в зависимости от введенных пользователем параметров.
        """
        # Запрашиваем у пользователя новую ширину и высоту
        new_width = simpledialog.askinteger("Новая ширина", "Введите новую ширину:")
        new_height = simpledialog.askinteger("Новая высота", "Введите новую высоту:")

        if new_width and new_height:
            # Обновляем размеры Canvas
            self.canvas.config(width=new_width, height=new_height)
            # Создаем новое изображение с обновленными размерами и белым фоном
            self.image = Image.new("RGB", (new_width, new_height), "white")
            self.draw = ImageDraw.Draw(self.image)

        # Переменная для отслеживания координат мыши
        self.last_x, self.last_y = None, None

    def add_text(self):
        """
        Запрашивает у пользователя текст и размещает его на холсте по клику мыши.
        """
        input_text = simpledialog.askstring("Ввод текста", "Введите текст:")
        if input_text:
            self.canvas.bind('<Button-1>', lambda event, text=input_text: self.draw_text(event, text))

    def draw_text(self, event, text):
        """
        Добавляет текст на картинку в заданных координатах, снимает биндинг.
        :param event: объект события, содержащий координаты клика
        :param text: текст для добавления на изображение
        """
        self.draw.text((event.x, event.y), text, fill=self.pen_color)
        self.canvas.create_text(event.x, event.y, anchor='nw', text=text, fill=self.pen_color, font=("Arial", 15))
        self.canvas.unbind('<Button-1>')  # Снятие биндинга после размещения текста

    def change_background_color(self):
        """
        Изменяет цвет фона на выбранный.
        """
        new_bg_color = colorchooser.askcolor(title="Выберите цвет фона")[1]
        if new_bg_color:
            self.canvas.config(bg=new_bg_color)
            # Новый холст с учетом нового фона
            self.image = Image.new("RGB", (self.canvas.winfo_width(), self.canvas.winfo_height()), new_bg_color)
            self.draw = ImageDraw.Draw(self.image)
            self.canvas_color = new_bg_color


def main():
    """
    Запуск основного окна интерфейса приложения.
    """
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
