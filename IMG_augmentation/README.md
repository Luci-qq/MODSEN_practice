# ImageAugmentationApp

Приложение для аугментации изображений.
Список поддерживаемых аугментаций:

- Crop (обрезка)
- Rotate (вращение)
- Contrast (настройки контрастности)
- Brightness (настройка яркости)
- Saturation (настройка насыщенности)
- Noise (добавление шума)
- Shift (смещение)
- Shear (сдвиг по горизонтали)
- Stretch (растяжение)
- Random Crop (случайная вырезка)
- Add text (добавление текста на изображение)

## Содержание

- [Технологии](#id_technologies)
- [Начало работы](#id_installation)

<a id='id_technologies'></a>

## Технологии

- [Kivy](https://kivy.org/)
- [Kivymd](https://kivymd.readthedocs.io/en/latest/index.html)
- [OpenCV](https://opencv.org/)
- [Pillow](https://python-pillow.org/)

<a id='id_installation'></a>

## Установка и запуск

1. Создание виртуального окружения:

```bash
python -m venv venv
```

2.  Активация виртуального окружения:

- Windows:

```sh
.\venv\Scripts\activate
```

- macOS и Linux:

```sh
source venv/bin/activate
```

3. Установка зависимостей:

```sh
pip install -r requirements.txt
```

4. Запуск приложения:

```sh
python main.py
```