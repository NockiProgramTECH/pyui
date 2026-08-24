"""Application de test — placement explicite (pack, grid, place)."""

from django.conf.locale import ro

from pyui import (
    App, Button, Label, Column, Frame, Input, Card, Theme,
)


def main():
    app = App(title="Mon application — test", size=(800, 600), theme="light")

    # Colonne principale (layout qui empile les enfants)
    
    frame =Frame(app,)
    frame.place(x =20,y=25)

    Label(frame,text ="Lankoande",color="red",anchor="w",).grid(row =0,column=0)


    app.run()


if __name__ == "__main__":
    main()
