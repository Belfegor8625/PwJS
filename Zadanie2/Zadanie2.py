#!/usr/bin/env python
# encoding: utf-8

import npyscreen

class FormFirst(npyscreen.ActionForm, npyscreen.SplitForm):

    def create(self):
        self.numberOfData = self.add(npyscreen.TitleText, name="Podaj ilosc danych do wprowadzenia: ")

    def on_ok(self):
        self.parentApp.getForm("ADDDATA").number = int(self.numberOfData.value)
        if int(self.numberOfData.value) > 0:
            self.parentApp.setNextForm("ADDDATA")
            self.editing = False
        else:
            exit()

    def on_cancel(self):
        exit()

class FormAddData(npyscreen.ActionForm,npyscreen.SplitForm):

    def create(self):
        self.show_aty=10
        self.nameAndSurname = self.add(npyscreen.TitleText, name="Podaj imie i nazwisko: ")
        self.number = 0

    def on_ok(self):
        self.saveData()
        self.checkNumberOfTimes()
        self.nameAndSurname.value = ""

    def on_cancel(self):
        exit()

    def checkNumberOfTimes(self):
        if self.number > 1:
            self.number = self.number-1
            self.parentApp.setNextForm("ADDDATA")
        else:
            self.parentApp.setNextForm("END")
            self.editing = False

    def saveData(self):
        self.parentApp.getForm("END").namesAndSurnamesList.append(self.nameAndSurname.value)

class FormChooseAndGetList(npyscreen.ActionForm,npyscreen.SplitForm):

    namesAndSurnamesList = []

    def create(self):
        self.option = self.add(npyscreen.TitleSelectOne, max_height=4, value=[0, ], name="Sortowanie wedlug",
                           values=["Imion", "Nazwisk", ], scroll_exit=True)

    def beforeEditing(self):
        npyscreen.blank_terminal()

    def on_ok(self):
        if self.option.value[0] == 0:
            npyscreen.notify_confirm(
                self.buildMessageString(sorted(self.divideNamesAndSurnames(self.namesAndSurnamesList), key=lambda x: x[0])),
                title="Po imieniu",wide=True)
        elif self.option.value[0] == 1:
            npyscreen.notify_confirm(
                self.buildMessageString(sorted(self.divideNamesAndSurnames(self.namesAndSurnamesList), key=lambda x: x[1])),
                title="Po nazwisku",wide=True)


    def on_cancel(self):
        exit()

    def divideNamesAndSurnames(self, list):
        newList = []
        for item in list:
            item = item.strip()
            item = item.split(" ")
            newList.append(item)
        return newList

    def buildMessageString(self, names):
        string = ""
        for value in names:
            string += value[0] + " " + value[1] + "\n"

        return string


class App(npyscreen.NPSAppManaged):

    def onStart(self):
        self.addForm("MAIN", FormFirst, name="Ilosc danych", lines=10, columns=40, draw_line_at=7)
        self.addForm("ADDDATA", FormAddData, name="Imie i nazwisko", lines=10, columns=50, draw_line_at=7)
        self.addForm("END", FormChooseAndGetList, name="Lista", lines=10, columns=50, draw_line_at=7)

if __name__ == "__main__":
    App = App()
    App.run()