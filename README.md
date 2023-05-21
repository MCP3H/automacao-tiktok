# Projeto Hunter
Uma ferramenta que utiliza inteligência artificial para criar uma base de links de vídeos. Ele emprega o modelo de rede neural convolucional YOLO para detectar objetos em vídeos do TikTok e registrar sua frequência de ocorrência. Além disso, o projeto também tem como objetivo auxiliar no desenvolvimento de novos modelos de inteligência artificial.

# Requisitos
Tela 1920 x 1080 FULL HD: A aplicação requer uma tela com essa resolução para capturar os quadros dos vídeos. O código não é otimizado para resoluções menores.

Placa Nvidia Geforce GTX 1060: Embora seja possível utilizar a CPU, é recomendado utilizar a GPU-CUDA para acelerar a predição dos quadros. É necessário instalar a versão compatível do Torch que corresponda à versão do driver da placa de vídeo. Confira este vídeo para configurar a CUDA na máquina: [PyTorch & CUDA Setup - Windows 10](https://www.youtube.com/watch?v=GMSjDTU8Zlc&ab_channel=CloudCasts-AlanSmith).
Observações: A versão do CUDA utilizada no projeto é a 12.1. Foi utilizado estes passos para configurar a CUDA na maquina:

1. Acesse o site da NVIDIA para instalar o recurso da CUDA 12.1: [developer.nvidia](https://developer.nvidia.com/cuda-downloads);
2. Execute o comando "nvidia-smi" no prompt de comando para verificar a versão do driver da placa e a versão do CUDA;
3. Acesse o site do [PyTorch](https://pytorch.org/) e instale o recurso da CUDA 12.1;
4. Execute o comando "pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu121" de acordo com as instruções do site;

# Configurar a aplicação - Windows

Linguagem de programação: O projeto foi desenvolvido em Python 3.9.6. Você pode baixar essa versão [aqui](https://www.python.org/downloads/release/python-396/).

Banco de dados: Para o gerenciamento do banco de dados, foi utilizado o MySQL Community. Você pode instalar a partir deste [link](https://dev.mysql.com/downloads/installer/). Na instalação personalizada, selecione apenas o conector do Python.

Configuração das tabelas do banco de dados: Execute o script "instalacao.sql" para criar as tabelas do projeto.

Clonar o projeto: Caso não tenha o Git instalado, você pode baixá-lo [aqui](https://git-scm.com/downloads).
Observações: Para clonar o projeto, siga estes passos:

1. Acesse a pasta onde deseja clonar o projeto (por exemplo: "cd C:\tcc");
2. Clique com o botão direito do mouse e selecione a opção "Git Bash Here";
3. Execute o comando "git clone https://github.com/MCP3H/automacao-tiktok.git" para baixar os arquivos do projeto;

Baixar as dependências do projeto: Utilize o arquivo "requirements.txt" para instalar as bibliotecas necessárias. Se preferir, você pode fazer backup das suas bibliotecas atuais e instalar apenas as do projeto seguindo estes passos:

1. Abra o prompt de comando (CMD);
2. Navegue até a pasta onde deseja criar o backup das bibliotecas (por exemplo: "cd C:\temp");
3. Execute o comando "pip freeze" para mostrar as bibliotecas instaladas atualmente;
4. Execute o comando "pip freeze > requirements.txt" para criar um arquivo com as bibliotecas atuais;
5. Execute o comando "pip uninstall -r requirements.txt -y" para desinstalar automaticamente as bibliotecas listadas no arquivo gerado;
6. Acesse a pasta do projeto clonado (por exemplo: "cd C:\tcc");
7. Execute o comando "pip install -r requirements.txt" para instalar as bibliotecas do projeto;

# Experimentos adicionais

Pré-experimento para definir o critério de aceitação: O arquivo "criterio_aceitacao.py" contém um experimento onde o modelo YOLOv5x avaliou 50 imagens, sendo 40 de cachorros e 10 de espécies parecidas (lobos, coiotes e raposas).

Identificação dos componentes da rede social TikTok: O arquivo "cursor_localizacao.py" foi utilizado para automatizar a aplicação na hora de clicar nas opções na tela, identificando os componentes da rede social.

Análise em tempo real do reconhecimento de objetos: O arquivo "reconhecimento_tempo_real.py" foi criado para verificar em tempo real a qualidade das predições do algoritmo YOLOv5.