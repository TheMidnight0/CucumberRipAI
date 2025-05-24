import cv2
import numpy as np
import torch

model = torch.hub.load('yolov5', 'custom', path="yolov5/runs/train/exp/weights/best.pt", source="local")
model.conf = 0.3
model.iou = 0.35

def conf_model(conf_thres: float | None = None, iou_thres: float | None = None):
    if conf_thres != None and conf_thres != model.conf:
        model.conf = conf_thres
    if iou_thres != None and iou_thres != model.iou:
        model.iou = iou_thres

def predict(image):
    # Конвертируем байты в numpy array
    np_img = np.frombuffer(image, np.uint8)
    # Декодируем изображение
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)  # BGR
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Выполняем инференс
    results = model(img, size=640) # type: ignore
    
    # Фильтруем по порогу уверенности
    results = results.pandas().xyxy[0]  # pandas DataFrame с результатами
    
    # Рисуем рамки и метки на исходном изображении (BGR)
    for _, row in results.iterrows():
        x1, y1, x2, y2 = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
        label = f"{row['name']} {row['confidence']:.2f}"
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    # Кодируем обратно в байты JPEG
    success, encoded_img = cv2.imencode('.jpg', cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    if not success:
        raise RuntimeError("Ошибка при кодировании изображения")
    
    return encoded_img.tobytes()