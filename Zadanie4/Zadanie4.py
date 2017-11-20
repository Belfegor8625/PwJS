#!/usr/bin/env python
# encoding: utf-8

import npyscreen
import urllib.request

"""         TODO 
obsluga funkcjonalnosci z test.py
zmiana klasy na student i poszerzenie jej
obsuga nowych separatorow danych

"""
class WorkerData(object):
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname

    def getName(self):
        return self.name

    def getSurname(self):
        return self.surname


allDataList = []


class ButtonExit(npyscreen.ButtonPress):
    def whenPressed(self):
        exit()


class ButtonPrevious(npyscreen.ButtonPress):
    def whenPressed(self):
        npyscreen.blank_terminal()
        self.parent.parentApp.switchFormPrevious()


class ButtonSaveBase(npyscreen.ButtonPress):
    def whenPressed(self):
        if self.parent.baseName.value is not None:
            self.baseName = self.parent.baseName.value
            file = open(self.baseName, "w")
            for item in allDataList:
                line = str(item.id) + " " + item.name + " " + item.surname + "\n"
                file.write(line)
            file.close()
            self.endOrContinue()
            self.parent.baseName.value = ""
        else:
            npyscreen.notify_confirm("Brak nazwy", "Error")

    def endOrContinue(self):
        option = npyscreen.notify_yes_no("Czy zakonczyc prace?", "Koniec")
        if option:
            exit()
        else:
            self.parent.parentApp.switchForm("MAIN")
            npyscreen.blank_terminal()


class FormFirst(npyscreen.FormBaseNew):
    def create(self):
        self.buttonNewBase = self.add(self.ButtonNewBase, name="Nowa baza")
        self.buttonLoadBase = self.add(self.ButtonLoadBase, name="Wczytaj baze")
        self.buttonExit = self.add(ButtonExit, name="Wyjscie")

    class ButtonNewBase(npyscreen.ButtonPress):
        def whenPressed(self):
            self.parent.parentApp.switchForm("NUMBEROFNEWDATA")

    class ButtonLoadBase(npyscreen.ButtonPress):
        dataList = []

        def whenPressed(self):
            the_selected_file = npyscreen.selectFile()
            file = open(the_selected_file, "r")
            try:
                for line in file:
                    self.dataList.append(line)
                    line = line.strip()
                    line = line.split(" ")
                    allDataList.append(WorkerData(line[0], line[1]))

            finally:
                file.close()
            npyscreen.blank_terminal()
            self.parent.parentApp.switchForm("BASEOPTIONS")


class FormNumberOfNewData(npyscreen.FormBaseNew):
    def create(self):
        self.numberOfData = self.add(npyscreen.TitleText, name="Podaj ilosc danych do wprowadzenia: ")
        self.buttonAddData = self.add(self.ButtonAddData, name="OK")
        self.buttonPrevious = self.add(ButtonPrevious, name="Powrot")

    class ButtonAddData(npyscreen.ButtonPress):
        def whenPressed(self):
            self.parent.parentApp.getForm("ADDDATA").number = int(self.parent.numberOfData.value)
            if int(self.parent.numberOfData.value) > 0:
                self.parent.parentApp.switchForm("ADDDATA")
                self.parent.parentApp.value = ""
            else:
                exit()


class FormAddData(npyscreen.FormBaseNew):
    def create(self):
        self.show_aty = 10
        self.nameAndSurname = self.add(npyscreen.TitleText, name="Podaj imie i nazwisko: ")
        self.buttonAdd = self.add(self.ButtonAdd, name="Dodaj")
        self.number = 0
        self.iterator = 1

    class ButtonAdd(npyscreen.ButtonPress):
        def whenPressed(self):
            self.parent.saveData()
            self.parent.checkNumberOfTimes()
            self.parent.nameAndSurname.value = ""

    def checkNumberOfTimes(self):
        if self.number > self.iterator:
            self.iterator = self.iterator + 1
            self.parentApp.setNextForm("ADDDATA")
            self.editing = False
        else:
            self.parentApp.setNextForm("BASEOPTIONS")
            self.editing = False

    def saveData(self):
        line = self.nameAndSurname.value.strip()

        line = line.split(" ")
        if allDataList:
            allDataList.append(WorkerData(len(allDataList) + 1, line[0], line[1]))
        else:
            allDataList.append(WorkerData(self.iterator, line[0], line[1]))


class FormSaveBase(npyscreen.FormBaseNew):
    def create(self):
        self.baseName = self.add(npyscreen.TitleText, name="Nazwa nowej bazy")
        self.buttonSaveBase = self.add(ButtonSaveBase, name="Zapisz")


class FormBaseOptions(npyscreen.FormBaseNew):
    def create(self):
        self.buttonShowBase = self.add(self.ButtonShowBase, name="Pokaz dane z bazy")
        self.buttonMoveToAddData = self.add(self.ButtonMoveToAddData, name="Dodaj nowe dane")
        self.buttonEraseData = self.add(self.ButtonGoToEraseData, name="Usun dane")
        self.buttonSave = self.add(self.ButtonGoToSaveBase, name="Zapisz dane")
        self.option = self.add(npyscreen.TitleSelectOne, max_height=4, value=[0, ], name="Sortowanie wedlug",
                               values=["Imion", "Nazwisk", ], scroll_exit=True)
        self.sort = self.add(self.ButtonSort, name="Pokaz posortowane")
        self.buttonExit = self.add(ButtonExit, name="Wyjscie")

    def beforeEditing(self):
        npyscreen.blank_terminal()

    class ButtonShowBase(npyscreen.ButtonPress):
        def whenPressed(self):
            npyscreen.notify_confirm("L.p.\tImie\tNazwisko\n" +
                                     self.parent.buildMessageString(allDataList),
                                     title="Baza danych", wide=True)

    class ButtonMoveToAddData(npyscreen.ButtonPress):
        def whenPressed(self):
            self.parent.parentApp.switchForm("NUMBEROFNEWDATA")

    class ButtonGoToSaveBase(npyscreen.ButtonPress):
        def whenPressed(self):
            self.parent.parentApp.switchForm("SAVEBASE")

    class ButtonSort(npyscreen.ButtonPress):
        def whenPressed(self):
            if self.parent.option.value[0] == 0:
                npyscreen.notify_confirm("L.p.\tImie\tNazwisko\n" +
                                         self.parent.buildMessageString(sorted(allDataList, key=WorkerData.getName)),
                                         title="Po imieniu", wide=True)
            elif self.parent.option.value[0] == 1:
                npyscreen.notify_confirm("L.p.\tImie\tNazwisko\n" +
                                         self.parent.buildMessageString(sorted(allDataList, key=WorkerData.getSurname)),
                                         title="Po nazwisku", wide=True)

    def buildMessageString(self, list):
        string = ""
        counter = 1
        for item in list:
            string += str(counter) + "\t" + item.name + "\t" + item.surname + "\n"
            counter = counter + 1
        return string

    class ButtonGoToEraseData(npyscreen.ButtonPress):
        def whenPressed(self):
            self.parent.parentApp.getForm("ERASEDATA").dataToErase.values = ['{} {}'.format(item.name,item.surname)
                                                                             for item in allDataList]
            self.parent.parentApp.switchForm("ERASEDATA")


class FormEraseData(npyscreen.ActionPopup):
    def create(self):
        self.dataToErase = self.add(npyscreen.TitleMultiSelect, max_height=7, name="Wybierz dane do usuniecia:",
                                    scroll_exit=True)

    def on_ok(self):
        selectedIndexes = self.dataToErase.value
        if selectedIndexes > 0:
            for index in selectedIndexes:
                allDataList.pop(index)
        else:
            npyscreen.notify_confirm("Nie wybrano danych do usuniecia", title="Blad")
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()


class App(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", FormFirst, name="Ekran startowy", lines=10, columns=40)
        self.addForm("BASEOPTIONS", FormBaseOptions, name="Opcje bazy", lines=15, columns=40)
        self.addForm("NUMBEROFNEWDATA", FormNumberOfNewData, name="Ilosc danych", lines=10, columns=40)
        self.addForm("ADDDATA", FormAddData, name="Imie i nazwisko", lines=10, columns=50)
        self.addForm("ERASEDATA", FormEraseData, name="Usuwanie danych", lines=20, columns=40)
        self.addForm("SAVEBASE", FormSaveBase, name="Zapis bazy", lines=10, columns=40)


if __name__ == "__main__":
    App = App()
    App.run()
