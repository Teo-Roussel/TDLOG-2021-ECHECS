## Imports
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

## Globals

global King
King = 0

global Queen
Queen = 1

global Tower
Tower = 2

global Knight
Knight = 3

global Bishop
Bishop = 4

global PawnL
PawnL = 5

global PawnR
PawnR = 6

global vecteurDeplIA
vecteurDeplIA = [
    [np.array([1, 1]), np.array([1, 0]), np.array([1, -1]), np.array([0, 1])],
    [np.array([1, 1]), np.array([1, 0]), np.array([1, -1]), np.array([0, 1])],
    [np.array([1, 0]), np.array([0, 1])],
    [np.array([1, 2]), np.array([2, 1]), np.array([2, -1]), np.array([1, -2])],
    [np.array([1, -1]), np.array([1, 1])],
    [np.array([1, 0])],
    [np.array([-1, 0])],
]

global vecteurDepl
vecteurDepl = [
    [np.array([1, 1]), np.array([0, 1]), np.array([-1, 1]), np.array([1, 0])],
    [np.array([1, 1]), np.array([0, 1]), np.array([-1, 1]), np.array([1, 0])],
    [np.array([0, 1]), np.array([1, 0])],
    [np.array([2, 1]), np.array([1, 2]), np.array([-1, 2]), np.array([-2, 1])],
    [np.array([-1, 1]), np.array([1, 1])],
    [np.array([0, 1])],
    [np.array([0, -1])],
]

global vecteurExt
vecteurExt = [2, 8, 8, 2, 8, 3, 3]

global vecteurExt2
vecteurExt2 = [-1, -7, -7, -1, -7, 0, 0]

global PiecesNames
PiecesNames = {
    Tower: "Images_IG/Tower_",
    Knight: "Images_IG/Knight_",
    Bishop: "Images_IG/Bishop_",
    Queen: "Images_IG/Queen_",
    King: "Images_IG/King_",
    PawnL: "Images_IG/Pawn_",
    PawnR: "Images_IG/Pawn_",
}

## Useful functions


def isAttacked(loc, TabA, coul):
    """
    Inputs :
        loc : np.array(size = (1,2), dtype = int) representing the a location on the chessboard (between (0,0) and (7,7))
        TabA : np.array(size = (8,8), dtype = PersonnalButton) the array representing buttons on a chessboard
        coul : int \in {1,2} corresponding to the olor you want to test
    Output :
        Bool indicating if a piece of TabA which color is col has the possibility of going to loc

    """
    for i in range(8):
        for j in range(8):
            try:
                piece = TabA[i, j].pieceAssoc
                if piece.couleur != coul:
                    AllpossibleDeplacement = piece.PossibleDeplacement(piece == King)
                    for dep in AllpossibleDeplacement[0]:
                        if tuple(loc) == tuple(dep):
                            return True
            except:
                pass
    return False


def FindKing(TabA, coul):
    """
    Inputs :
        TabA : np.array(size = (8,8), dtype = PersonnalButton) the array representing buttons on a chessboard
        coul : int \in {1,2} corresponding to the color you want to test
    Output :
        int*int representing line and column on which the king of color coul is on in TabA. Matrix indexes notation for location
    """
    found = False
    i = 0
    while i < 8 and not found:
        j = 0
        while j < 8 and not found:
            try:
                if (
                    TabA[i, j].pieceAssoc.piece == 0
                    and TabA[i, j].pieceAssoc.couleur == coul
                ):
                    found = True
            except:
                pass
            j += 1
        i += 1
    iking, jking = i - 1, j - 1
    return (iking, jking)


def check(TabA, coul):
    """
    Inputs :
        TabA : np.array(size = (8,8), dtype = PersonnalButton) the array representing buttons on a chessboard
        coul : int \in {1,2} corresponding to the color you want to test
    Output :
        bool stating whther king of color coul is in a checked position
    """
    # Finding the king
    iking, jking = FindKing(TabA, coul)
    # Check
    check = isAttacked(np.array([iking, jking]), TabA, coul)
    return check


def CancelMov(Tab, DamierLinked, loc, formerloc, pieceTaken=None):
    """
    Inputs :
        TabA : np.array(size = (8,8), dtype = PersonnalButton) the array representing buttons on a chessboard
        DamierLinked : Damier object
        loc : np.array(size = (1,2), dtype = int) representing the location on the chessboard (between (0,0) and (7,7))
        formerloc : np.array(size = (1,2), dtype = int) representing the location on the chessboard (between (0,0) and (7,7))
    Kwargs :
        pieceTaken : Piece object
    Output :
        Cancel in Tab and DamierLinked the movement from formeroc to loc that has taken pieceTaken
    """

    # ================== Getting piece to move ===================#
    locationPieceToMove = loc
    PersButtToMove = Tab[locationPieceToMove[0], locationPieceToMove[1]]
    FormerButt = Tab[formerloc[0], formerloc[1]]

    # ================== Printing at former location ====================#
    name = (
        PiecesNames[PersButtToMove.pieceAssoc.piece]
        + ("N" if PersButtToMove.pieceAssoc.couleur == 1 else "B")
        + ("N" if np.sum(FormerButt.location) % 2 == 1 else "B")
        + ".PNG"
    )
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(name), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    FormerButt.button.setIcon(icon)
    FormerButt.pieceAssoc = PersButtToMove.pieceAssoc
    FormerButt.pieceAssoc.localisation = formerloc
    DamierLinked.Dam[
        2 + FormerButt.location[0], 2 + FormerButt.location[1]
    ] = PersButtToMove.pieceAssoc.couleur

    # ============== Removing from location ===============#
    if pieceTaken == None:
        PersButtToMove.button.setIcon(
            DamierLinked.icon1
            if np.sum(PersButtToMove.location) % 2 == 0
            else DamierLinked.icon2
        )
        DamierLinked.Dam[
            2 + PersButtToMove.location[0], 2 + PersButtToMove.location[1]
        ] = 0
        PersButtToMove.pieceAssoc = None

    # ========= Printing Taken Piece at Location ==========#
    else:
        name = (
            PiecesNames[pieceTaken.piece]
            + ("N" if pieceTaken.couleur == 1 else "B")
            + ("N" if np.sum(pieceTaken.localisation) % 2 == 1 else "B")
            + ".PNG"
        )
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(name), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        PersButtToMove.button.setIcon(icon)
        PersButtToMove.pieceAssoc = pieceTaken
        DamierLinked.Dam[
            2 + PersButtToMove.location[0], 2 + PersButtToMove.location[1]
        ] = pieceTaken.couleur

    # ========= Extension Pawns ==========#
    if FormerButt.pieceAssoc.piece == PawnL:
        extSupp = (FormerButt.pieceAssoc.PVP and FormerButt.location[1] == 1) or (
            not FormerButt.pieceAssoc.PVP and FormerButt.location[0] == 1
        )
        FormerButt.pieceAssoc.finExt = 2 + extSupp

    elif FormerButt.pieceAssoc.piece == PawnR:
        extSupp = (FormerButt.pieceAssoc.PVP and FormerButt.location[1] == 6) or (
            not FormerButt.pieceAssoc.PVP and FormerButt.location[0] == 6
        )

        FormerButt.pieceAssoc.finExt = 2 + extSupp


def DeplacementCopy(Tab, ancientLoc, newLoc):
    """
    Inputs :
        TabA : np.array(size = (8,8), dtype = PersonnalButton) the array representing buttons on a chessboard
        newLoc : np.array(size = (1,2), dtype = int) representing a location on the chessboard (between (0,0) and (7,7))
        ancientLoc : np.array(size = (1,2), dtype = int) representing a location on the chessboard (between (0,0) and (7,7))
    Output :
        Simulates the move from ancienLoc to newLoxc in Tab WITHOUT it being shown in the GI
    """

    # ================== Getting piece to move ===================#
    locationPieceToMove = ancientLoc
    PersButtToMove = Tab[locationPieceToMove[0], locationPieceToMove[1]]
    PieceToReturn = Tab[newLoc[0], newLoc[1]].pieceAssoc
    PersButtonMoved = Tab[newLoc[0], newLoc[1]]

    # ================== Updating ChessPlate ===================#
    PersButtonMoved.pieceAssoc = Piece(
        PersButtToMove.pieceAssoc.DamAssoc,
        PersButtToMove.pieceAssoc.piece,
        PersButtToMove.pieceAssoc.couleur,
        PersButtonMoved.location,
        Tab,
        PersButtToMove.fenetreAssoc.PVP,
    )
    PersButtonMoved.pieceAssoc.DamAssoc.Dam[
        2 + PersButtToMove.location[0], 2 + PersButtToMove.location[1]
    ] = 0
    PersButtonMoved.pieceAssoc.DamAssoc.Dam[
        2 + PersButtonMoved.location[0], 2 + PersButtonMoved.location[1]
    ] = PersButtToMove.pieceAssoc.couleur
    PersButtToMove.pieceAssoc = None
    return PieceToReturn


def checkMate(Win, coul):
    """
    Inputs :
        Win : Ui_PlayWindow object
        coul : int \in {1,2} corresponding to the color you want to test
    Output :
        bool stating whether there a checkmate for color @param coul
    """
    checkmate = check(Win.Tab, coul)
    i = 0
    while i < 8 and checkmate:
        j = 0
        while j < 8 and checkmate:
            try:
                piece = Win.Tab[i, j].pieceAssoc
                if piece.couleur == coul:
                    AllpossibleDeplacement = piece.PossibleDeplacement(piece == King)
                    for dep in AllpossibleDeplacement[0]:
                        pieceTaken = DeplacementCopy(Win.Tab, np.array([i, j]), dep)
                        if not check(Win.Tab, coul):
                            checkmate = False
                        CancelMov(
                            Win.Tab, Win.Damier, dep, np.array([i, j]), pieceTaken
                        )
            except:
                pass
            j += 1
        i += 1
    return checkmate


def Pat(Win, coul):
    """
    Inputs :
        Win : Ui_PlayWindow object
        coul : int \in {1,2} corresponding to the color you want to test
    Output :
        bool stating whether there a pat for color @param coul
    """
    pat = not check(Win.Tab, coul)
    i = 0
    while i < 8 and pat:
        j = 0
        while j < 8 and pat:
            try:
                piece = Win.Tab[i, j].pieceAssoc
                if piece.couleur == coul:
                    AllpossibleDeplacement = piece.PossibleDeplacement(piece == King)
                    for dep in AllpossibleDeplacement[0]:
                        pieceTaken = DeplacementCopy(Win.Tab, np.array([i, j]), dep)
                        if not check(Win.Tab, coul):
                            pat = False
                        CancelMov(
                            Win.Tab, Win.Damier, dep, np.array([i, j]), pieceTaken
                        )
            except:
                pass
            j += 1
        i += 1
    return pat


## Classes


class Piece:
    """
    Class representing a piece on a square of the chessboard
    """

    def __init__(self, Dam, numero, couleur, localisation, TabAssoc, PVP):
        """
        Init method
        Inputs :
            Dam : Damier Object that will be linked to the Piece
            numero : int \in [0,6] representing a piece (confere globals to know the corresponding pieces)
            couleur : color of the chose piece \in {1 being black, 2 being white}
            localisation : np.array(size = (1,2), dtype = int) representing a location on the chessboard (between (0,0) and (7,7))
            TabA : np.array(size = (8,8), dtype = PersonnalButton) an array representing buttons on a chessboard that will be linked to the Piece

        """
        self.PVP = PVP
        self.DamAssoc = Dam
        self.piece = numero
        self.couleur = couleur
        self.vecDepl = vecteurDepl[numero] if PVP else vecteurDeplIA[numero]
        self.debExt = vecteurExt2[numero]
        self.finExt = vecteurExt[numero]
        self.localisation = localisation
        self.TabAssoc = TabAssoc

        if self.piece == PawnL:
            extSupp = (self.PVP and self.localisation[1] == 1) or (
                not self.PVP and self.localisation[0] == 1
            )
            self.finExt = 2 + extSupp

        if self.piece == PawnR:
            extSupp = (self.PVP and self.localisation[1] == 6) or (
                not self.PVP and self.localisation[0] == 6
            )
            self.finExt = 2 + extSupp

    def PossibleDeplacement(self, testCastle):
        """
        Input :
            testCastle : bool
        Output :
            Generates all possible movements of the Piece on the Damier associated
            Takes castles in consideration if testCastle == True
            Remember that it generates ALL deplacements not only legit deplacements.
            For that please refer to Play_Window.PersonnalButton.LightenPossibleDeplacement
        """
        possibleList = []
        isCastle = []
        k = 0
        while k < len(self.vecDepl):

            # =============== Marche Avant ================#
            boolInterrupt = False
            vec = self.vecDepl[k]
            i = 1
            while not boolInterrupt and i < self.finExt:
                realvec = i * vec
                posfin = self.localisation + realvec
                if self.DamAssoc.Dam[2 + posfin[0], 2 + posfin[1]] == 0:
                    possibleList += [posfin]

                elif (
                    self.DamAssoc.Dam[2 + posfin[0], 2 + posfin[1]] == self.couleur
                    or self.DamAssoc.Dam[2 + posfin[0], 2 + posfin[1]] == -1
                ):
                    boolInterrupt = True

                else:
                    boolInterrupt = True
                    possibleList += (
                        [posfin] if self.piece != PawnL and self.piece != PawnR else []
                    )  # Le pion ne peut ni manger en avant ni en arrière

                i += 1
            # =============== Marche Arrière ================#
            i = -1
            boolInterrupt = False
            while not boolInterrupt and i >= self.debExt:
                realvec = i * vec
                posfin = self.localisation + realvec
                if self.DamAssoc.Dam[2 + posfin[0], 2 + posfin[1]] == 0:
                    possibleList += [posfin]

                elif (
                    self.DamAssoc.Dam[2 + posfin[0], 2 + posfin[1]] == self.couleur
                    or self.DamAssoc.Dam[2 + posfin[0], 2 + posfin[1]] == -1
                ):
                    boolInterrupt = True

                else:
                    boolInterrupt = True
                    possibleList += (
                        [posfin] if self.piece != PawnL and self.piece != PawnR else []
                    )  # Le pion ne peut ni manger en avant ni en arrière

                i -= 1

            k += 1

        # =============== Castle ================#
        if self.piece == King and testCastle:
            isCastle = self.CastleAllowed()

        # =============== Pawns ================#
        if self.piece == PawnR:

            if (
                self.DamAssoc.Dam[
                    2 + self.localisation[0] + (1 if self.PVP else -1),
                    2 + self.localisation[1] + (-1 if self.PVP else 1),
                ]
                != -1
                and self.DamAssoc.Dam[
                    2 + self.localisation[0] + (1 if self.PVP else -1),
                    2 + self.localisation[1] + (-1 if self.PVP else 1),
                ]
                != 0
                and self.DamAssoc.Dam[
                    2 + self.localisation[0] + (1 if self.PVP else -1),
                    2 + self.localisation[1] + (-1 if self.PVP else 1),
                ]
                != self.couleur
            ):
                possibleList += [
                    (
                        self.localisation[0] + (1 if self.PVP else -1),
                        self.localisation[1] + (-1 if self.PVP else 1),
                    )
                ]

            if (
                self.DamAssoc.Dam[
                    2 + self.localisation[0] - 1, 2 + self.localisation[1] - 1
                ]
                != -1
                and self.DamAssoc.Dam[
                    2 + self.localisation[0] - 1, 2 + self.localisation[1] - 1
                ]
                != 0
                and self.DamAssoc.Dam[
                    2 + self.localisation[0] - 1, 2 + self.localisation[1] - 1
                ]
                != self.couleur
            ):
                possibleList += [(self.localisation[0] - 1, self.localisation[1] - 1)]

        if self.piece == PawnL:

            if (
                self.DamAssoc.Dam[
                    2 + self.localisation[0] + 1, 2 + self.localisation[1] + 1
                ]
                != -1
                and self.DamAssoc.Dam[
                    2 + self.localisation[0] + 1, 2 + self.localisation[1] + 1
                ]
                != 0
                and self.DamAssoc.Dam[
                    2 + self.localisation[0] + 1, 2 + self.localisation[1] + 1
                ]
                != self.couleur
            ):
                possibleList += [(self.localisation[0] + 1, self.localisation[1] + 1)]

            if (
                self.DamAssoc.Dam[
                    2 + self.localisation[0] + (-1 if self.PVP else 1),
                    2 + self.localisation[1] + 1 + (1 if self.PVP else -1),
                ]
                != -1
                and self.DamAssoc.Dam[
                    2 + self.localisation[0] + (-1 if self.PVP else 1),
                    2 + self.localisation[1] + (1 if self.PVP else -1),
                ]
                != 0
                and self.DamAssoc.Dam[
                    2 + self.localisation[0] + (-1 if self.PVP else 1),
                    2 + self.localisation[1] + (1 if self.PVP else -1),
                ]
                != self.couleur
            ):
                possibleList += [
                    (
                        self.localisation[0] + (-1 if self.PVP else 1),
                        self.localisation[1] + (1 if self.PVP else -1),
                    )
                ]

        return (possibleList, isCastle)

    def CastleAllowed(self):
        """
        Method that generated the possible castles for the Piece object
        """

        CastleDeplacement = []
        if self.PVP:
            # ======================| Castle for Black pieces |======================#

            if self.localisation[0] == 4 and self.localisation[1] == 0:

                # -------------------| Grand Castle |-------------------#
                if self.DamAssoc.CastleBGrand == True:
                    if (
                        self.DamAssoc.Dam[2 + 1, 2 + 0] == 0
                        and self.DamAssoc.Dam[2 + 2, 2 + 0] == 0
                        and self.DamAssoc.Dam[2 + 3, 2 + 0] == 0
                        and self.TabAssoc[0, 0].pieceAssoc.piece == Tower
                    ):
                        if (
                            not isAttacked(
                                np.array([1, 0]), self.TabAssoc, self.couleur
                            )
                            and not isAttacked(
                                np.array([2, 0]), self.TabAssoc, self.couleur
                            )
                            and not isAttacked(
                                np.array([3, 0]), self.TabAssoc, self.couleur
                            )
                            and not isAttacked(
                                self.localisation, self.TabAssoc, self.couleur
                            )
                        ):
                            CastleDeplacement += [np.array([2, 0])]

                # -------------------| Small Castle |-------------------#
                if self.DamAssoc.CastleBSmall:
                    if (
                        self.DamAssoc.Dam[2 + 5, 2 + 0] == 0
                        and self.DamAssoc.Dam[2 + 6, 2 + 0] == 0
                        and self.TabAssoc[7, 0].pieceAssoc.piece == Tower
                    ):
                        if (
                            not isAttacked(
                                np.array([5, 0]), self.TabAssoc, self.couleur
                            )
                            and not isAttacked(
                                np.array([6, 0]), self.TabAssoc, self.couleur
                            )
                            and not isAttacked(
                                self.localisation, self.TabAssoc, self.couleur
                            )
                        ):
                            CastleDeplacement += [np.array([6, 0])]

            # ======================| Castle for White pieces |======================#

            elif self.localisation[0] == 4 and self.localisation[1] == 7:

                # -------------------| Grand Castle |-------------------#
                if self.DamAssoc.CastleWGrand == True:
                    if (
                        self.DamAssoc.Dam[2 + 1, 2 + 7] == 0
                        and self.DamAssoc.Dam[2 + 2, 2 + 7] == 0
                        and self.DamAssoc.Dam[2 + 3, 2 + 7] == 0
                        and self.TabAssoc[0, 7].pieceAssoc.piece == Tower
                    ):
                        if (
                            not isAttacked(
                                np.array([1, 7]), self.TabAssoc, self.couleur
                            )
                            and not isAttacked(
                                np.array([2, 7]), self.TabAssoc, self.couleur
                            )
                            and not isAttacked(
                                np.array([3, 7]), self.TabAssoc, self.couleur
                            )
                            and not isAttacked(
                                self.localisation, self.TabAssoc, self.couleur
                            )
                        ):
                            CastleDeplacement += [np.array([2, 7])]

                # -------------------| Small Castle |-------------------#
                if self.DamAssoc.CastleWSmall == True:
                    if (
                        self.DamAssoc.Dam[2 + 5, 2 + 7] == 0
                        and self.DamAssoc.Dam[2 + 6, 2 + 7] == 0
                        and self.TabAssoc[7, 7].pieceAssoc.piece == Tower
                    ):
                        if (
                            not isAttacked(
                                np.array([5, 7]), self.TabAssoc, self.couleur
                            )
                            and not isAttacked(
                                np.array([6, 7]), self.TabAssoc, self.couleur
                            )
                            and not isAttacked(
                                self.localisation, self.TabAssoc, self.couleur
                            )
                        ):
                            CastleDeplacement += [np.array([6, 7])]

        else:
            if self.TabAssoc[0, 0].fenetreAssoc.colorIA == 1:
                # ======================| Castle for Black pieces |======================#
                if self.couleur == 1 and self.piece == King:
                    lineKing = self.localisation[0]
                    # -------------------| Grand Castle |-------------------#
                    if self.DamAssoc.CastleBGrand == True:
                        if (
                            self.DamAssoc.Dam[2 + lineKing, 2 + 1] == 0
                            and self.DamAssoc.Dam[2 + lineKing, 2 + 2] == 0
                            and self.DamAssoc.Dam[2 + lineKing, 2 + 3] == 0
                            and self.TabAssoc[0, 0].pieceAssoc.piece == Tower
                        ):
                            if (
                                not isAttacked(
                                    np.array([lineKing, 1]), self.TabAssoc, self.couleur
                                )
                                and not isAttacked(
                                    np.array([lineKing, 2]), self.TabAssoc, self.couleur
                                )
                                and not isAttacked(
                                    np.array([lineKing, 3]), self.TabAssoc, self.couleur
                                )
                                and not isAttacked(
                                    self.localisation, self.TabAssoc, self.couleur
                                )
                            ):
                                CastleDeplacement += [np.array([lineKing, 2])]

                    # -------------------| Small Castle |-------------------#
                    if self.DamAssoc.CastleBSmall == True:
                        if (
                            self.DamAssoc.Dam[2 + lineKing, 2 + 5] == 0
                            and self.DamAssoc.Dam[2 + lineKing, 2 + 6] == 0
                            and self.TabAssoc[lineKing, 7].pieceAssoc.piece == Tower
                        ):
                            if (
                                not isAttacked(
                                    np.array([lineKing, 5]), self.TabAssoc, self.couleur
                                )
                                and not isAttacked(
                                    np.array([lineKing, 6]), self.TabAssoc, self.couleur
                                )
                                and not isAttacked(
                                    self.localisation, self.TabAssoc, self.couleur
                                )
                            ):
                                CastleDeplacement += [np.array([lineKing, 6])]

                # ======================| Castle for Whites pieces |======================#
                elif self.couleur == 2 and self.piece == King:
                    lineKing = self.localisation[0]
                    # -------------------| Grand Castle |-------------------#
                    if self.DamAssoc.CastleWGrand == True:
                        if (
                            self.DamAssoc.Dam[2 + lineKing, 2 + 1] == 0
                            and self.DamAssoc.Dam[2 + lineKing, 2 + 2] == 0
                            and self.DamAssoc.Dam[2 + lineKing, 2 + 3] == 0
                            and self.TabAssoc[lineKing, 0].pieceAssoc.piece == Tower
                        ):
                            if (
                                not isAttacked(
                                    np.array([lineKing, 1]), self.TabAssoc, self.couleur
                                )
                                and not isAttacked(
                                    np.array([lineKing, 2]), self.TabAssoc, self.couleur
                                )
                                and not isAttacked(
                                    np.array([lineKing, 3]), self.TabAssoc, self.couleur
                                )
                                and not isAttacked(
                                    self.localisation, self.TabAssoc, self.couleur
                                )
                            ):
                                CastleDeplacement += [np.array([lineKing, 2])]

                    # -------------------| Small Castle |-------------------#
                    if self.DamAssoc.CastleWSmall:
                        if (
                            self.DamAssoc.Dam[2 + lineKing, 2 + 5] == 0
                            and self.DamAssoc.Dam[2 + lineKing, 2 + 6] == 0
                            and self.TabAssoc[lineKing, 7].pieceAssoc.piece == Tower
                        ):
                            if (
                                not isAttacked(
                                    np.array([lineKing, 5]), self.TabAssoc, self.couleur
                                )
                                and not isAttacked(
                                    np.array([lineKing, 6]), self.TabAssoc, self.couleur
                                )
                                and not isAttacked(
                                    self.localisation, self.TabAssoc, self.couleur
                                )
                            ):
                                CastleDeplacement += [np.array([lineKing, 6])]

            else:
                # ======================| Castle for Black pieces |======================#
                if self.couleur == 1 and self.piece == King:
                    lineKing = self.localisation[0]
                    # -------------------| Grand Castle |-------------------#
                    if self.DamAssoc.CastleBGrand == True:
                        if (
                            self.DamAssoc.Dam[2 + lineKing, 2 + 4] == 0
                            and self.DamAssoc.Dam[2 + lineKing, 2 + 5] == 0
                            and self.DamAssoc.Dam[2 + lineKing, 2 + 6] == 0
                            and self.TabAssoc[0, 7].pieceAssoc.piece == Tower
                        ):
                            if (
                                not isAttacked(
                                    np.array([lineKing, 4]), self.TabAssoc, self.couleur
                                )
                                and not isAttacked(
                                    np.array([lineKing, 5]), self.TabAssoc, self.couleur
                                )
                                and not isAttacked(
                                    np.array([lineKing, 6]), self.TabAssoc, self.couleur
                                )
                                and not isAttacked(
                                    self.localisation, self.TabAssoc, self.couleur
                                )
                            ):
                                CastleDeplacement += [np.array([lineKing, 5])]

                    # -------------------| Small Castle |-------------------#
                    if self.DamAssoc.CastleBSmall == True:
                        if (
                            self.DamAssoc.Dam[2 + lineKing, 2 + 1] == 0
                            and self.DamAssoc.Dam[2 + lineKing, 2 + 2] == 0
                            and self.TabAssoc[lineKing, 0].pieceAssoc.piece == Tower
                        ):
                            if (
                                not isAttacked(
                                    np.array([lineKing, 1]), self.TabAssoc, self.couleur
                                )
                                and not isAttacked(
                                    np.array([lineKing, 2]), self.TabAssoc, self.couleur
                                )
                                and not isAttacked(
                                    self.localisation, self.TabAssoc, self.couleur
                                )
                            ):
                                CastleDeplacement += [np.array([lineKing, 1])]

                # ======================| Castle for Whites pieces |======================#
                elif self.couleur == 2 and self.piece == King:
                    lineKing = self.localisation[0]
                    self.lineKing = self.localisation[0]
                    # -------------------| Grand Castle |-------------------#
                    if self.DamAssoc.CastleWGrand == True:
                        if (
                            self.DamAssoc.Dam[2 + lineKing, 2 + 4] == 0
                            and self.DamAssoc.Dam[2 + lineKing, 2 + 5] == 0
                            and self.DamAssoc.Dam[2 + lineKing, 2 + 6] == 0
                            and self.TabAssoc[lineKing, 7].pieceAssoc.piece == Tower
                        ):
                            if (
                                not isAttacked(
                                    np.array([lineKing, 4]), self.TabAssoc, self.couleur
                                )
                                and not isAttacked(
                                    np.array([lineKing, 5]), self.TabAssoc, self.couleur
                                )
                                and not isAttacked(
                                    np.array([lineKing, 6]), self.TabAssoc, self.couleur
                                )
                                and not isAttacked(
                                    self.localisation, self.TabAssoc, self.couleur
                                )
                            ):
                                CastleDeplacement += [np.array([lineKing, 5])]

                    # -------------------| Small Castle |-------------------#
                    if self.DamAssoc.CastleWSmall:
                        if (
                            self.DamAssoc.Dam[2 + lineKing, 2 + 1] == 0
                            and self.DamAssoc.Dam[2 + lineKing, 2 + 2] == 0
                            and self.TabAssoc[lineKing, 0].pieceAssoc.piece == Tower
                        ):
                            if (
                                not isAttacked(
                                    np.array([lineKing, 1]), self.TabAssoc, self.couleur
                                )
                                and not isAttacked(
                                    np.array([lineKing, 2]), self.TabAssoc, self.couleur
                                )
                                and not isAttacked(
                                    self.localisation, self.TabAssoc, self.couleur
                                )
                            ):
                                CastleDeplacement += [np.array([lineKing, 1])]

        return CastleDeplacement


class Damier:
    """
    Class allowing to stock :
        Color of pieces on the chessboard for generating movement in Piece Class
        Castles allowed
        Icons corresponding to empty squares
    Allows to know if LEGIT game is null
    Utilitary class that MUST be used through Ui_PlayWindow since it is initialised
    as an empty Chessboard
    """

    def __init__(self, PVP, icon1, icon2):
        """
        Init method
        Inputs :
            PVP : bool allowing to know which mode is being played
            icon1 : QIcon for an empty white case
            icon2 : QIcon for an empty black case
        """
        self.Dam = np.zeros((12, 12), dtype=int)
        self.CastleWGrand = True
        self.CastleWSmall = True
        self.CastleBGrand = True
        self.CastleBSmall = True
        self.CastleWGrand_Save = None
        self.CastleWSmall_Save = None
        self.CastleBGrand_Save = None
        self.CastleBSmall_None = None
        self.PVP = PVP
        self.icon1 = icon1
        self.icon2 = icon2
        self.Initialise()

    def Initialise(self):
        """
        Initialises an empty chessboard. No piece on square being represented by a -1
        """
        for i in range(0, 12):
            for j in range(0, 12):
                if i < 2 or j < 2 or j >= 10 or i >= 10:
                    self.Dam[i, j] = -1

    def NullGame(self):
        """
        Method returning a bool indicating if only the two kings remain on board
        """
        nbWhite = 0
        nbBlack = 0
        for k in range(2, 8 + 2):
            L = list(self.Dam[k])
            nbWhite += L.count(2)
            nbBlack += L.count(1)
        return nbWhite == 1 and nbBlack == 1
