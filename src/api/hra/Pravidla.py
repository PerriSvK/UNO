from api.util.Task import Task
from gui.core.Anim import Anim
from gui.core.AnimInfo import AnimInfo
from src.api.hra.Farba import Farba
from src.api.hra.Hodnota import Hodnota


class Pravidla:
    @staticmethod
    def moze_polozit(ko, kd):
        #return ((ko.hodnota != Hodnota.PLUS4 and ko.hodnota != Hodnota.PLUS2 and ko.hodnota != Hodnota.ZMENA) and (ko.farba == kd.farba or ko.hodnota == kd.hodnota or ko.farba == Farba.BLACK or kd.farba == Farba.BLACK)) or (ko.hodnota == Hodnota.PLUS4 and kd.hodnota == Hodnota.PLUS4) or (ko.hodnota == Hodnota.PLUS2 and kd.hodnota == Hodnota.PLUS2)

        return ko.farba == kd.farba or ko.hodnota == kd.hodnota or kd.farba == Farba.BLACK #or kd.farba == Farba.BLACK

    @staticmethod
    def vykonaj_akciu(hra, karta):
        if karta.hodnota == Hodnota.REV:
            hra.zmena_smeru()

        if karta.hodnota == Hodnota.PLUS2:
            a = 0
            for i in range(2):
                k = hra.tahaci().vrchna()
                hra.hrac_po_smere().ruka().pridaj_kartu(k)
                hra.okno.handler.program.scheduler.add_task(Task(hra.okno.otoc_kartu, [k, hra.hrac_po_smere().id]), a)
                anim = AnimInfo(hra.hrac_po_smere(), k, hra.hrac_po_smere().ruka().pozicia, Anim.FORCE_PICK, 10)
                hra.okno.handler.program.scheduler.add_task(Task(hra.okno.pridaj_animaciu, [anim, True]), a+5)

                if not hra.hrac_po_smere().id:
                    hra.okno.handler.program.scheduler.add_task(Task(hra.okno.obrat_kartu, [k, hra.hrac_po_smere().id]), a+20)

                a += 30

            hra.okno.handler.program.scheduler.add_task(Task(hra.okno.uprac_ruku, [hra.hrac_po_smere().id]), a + 60)
            hra.skip()
            return True

        if karta.hodnota == Hodnota.PLUS4:
            a = 0
            for i in range(4):
                k = hra.tahaci().vrchna()
                hra.hrac_po_smere().ruka().pridaj_kartu(k)
                hra.okno.handler.program.scheduler.add_task(Task(hra.okno.otoc_kartu, [k, hra.hrac_po_smere().id]), a)
                anim = AnimInfo(hra.hrac_po_smere(), k, hra.hrac_po_smere().ruka().pozicia, Anim.FORCE_PICK, 10)
                hra.okno.handler.program.scheduler.add_task(Task(hra.okno.pridaj_animaciu, [anim, True]), a+5)

                if not hra.hrac_po_smere().id:
                    hra.okno.handler.program.scheduler.add_task(Task(hra.okno.obrat_kartu, [k, hra.hrac_po_smere().id]), a+20)

                a += 30

            hra.okno.handler.program.scheduler.add_task(Task(hra.okno.uprac_ruku, [hra.hrac_po_smere().id]), a + 60)
            hra.skip()
            return True

        if karta.hodnota == Hodnota.SKIP:
            hra.skip()

        return False