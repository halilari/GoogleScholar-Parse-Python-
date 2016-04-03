class Author:
    AdiSoyadi=""
    CalismaYeri=""
    ToplamAlintilanma=""
    ilgiAlanlari=[]
    Makaleleri=[]
    Katki=[]
    def __init__(self,AdiSoyadi):
        self.AdiSoyadi=AdiSoyadi
    def getAdiSoyadi(self):
        return self.AdiSoyadi
    def getCalismayeri(self):
        return self.CalismaYeri
    def getToplamAlintilanma(self):
        return self.ToplamAlintilanma
    def getİlgiAlani(self):
        return self.ilgiAlanlari
    def setAdiSoyadi(gelenAd):
        AdiSoyadi=gelenAd
    def setCalismaYeri(self,gelen):
        self.CalismaYeri=gelen

