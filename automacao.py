import funcoespyautogui as pya
import funcoesdb as db

pya.abrirTiktok()
pya.abrirMidia()

videoURL = pya.copiarLinkVideo()
db.salvarVideo(videoURL)

db.fecharConexao()
