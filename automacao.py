import funcoespyautogui as pya
import funcoesdb as db

pya.abrirTiktok()
pya.abrirMidia()

pya.passarVideo()
pya.curtirVideo()

videoURL = pya.copiarLinkVideo()
# db.salvarVideo(videoURL)

pya.fecharMidia()
db.fecharConexao()
