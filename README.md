# automacao-tiktok
TCC

# SELENIUM #
descobrir a versão do chrome que usaremos e baixar path nesse link:
https://sites.google.com/chromium.org/driver/downloads

# YOLOV5(You Only Look Once) #
modelo popular de detecção de objetos e segmentação de imagens 
Em 2021, a Ultralytics lançou o YOLOv5 , que melhorou ainda mais o desempenho do modelo e adicionou novos recursos, como suporte para segmentação panóptica e rastreamento de objetos.

pip install torch==1.8.1+cu111 torchvision==0.9.1+cu111 torchaudio===0.8.1 -f https://download.pytorch.org/whl/lts/1.8/torch_lts.html
git clone https://github.com/ultralytics/yolov5
cd yolov5
pip install -r requirements.txt
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')