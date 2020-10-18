# magisterka

Projekt opisywania obrazów za pomocą języka naturalnego, w których obiekty zostały odnalezione przy pomocy YOLOv3 (https://github.com/eriklindernoren/PyTorch-YOLOv3/blob/master/README.md)

1)
Plik detect.py jest częścią YOLOv3 został dostosowany do projektu, generuje opisy w postaci JSON-ów, które potem są wykorzystywane przez inne pliki.
2)
location_descirpiton.py
Plik jest używany do opisywania elementów wykrytych przez YOLO zapisanych w formacie json. 
3)
draw_picture_with_boxes.py
Plik wykorzystywany do wyświetlania samych bounding boxów na podstawie pliku json.
