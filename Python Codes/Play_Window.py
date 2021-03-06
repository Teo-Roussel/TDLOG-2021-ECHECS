## Imports

from PyQt5 import QtCore, QtGui, QtWidgets
from Play_Damier import Damier, Piece
from Play_Damier import King, Queen, Tower, Knight, Bishop, PawnL, PawnR
import Play_Damier as pld
import numpy as np
import moduleAI as p11m
import Enreg_Window as ErW
import HandleFiles as HdF
import AI_Level as AiL


## Globals

global InitBlack
InitBlack = [
    "Images_IG/Tower_NB.PNG",
    "Images_IG/Knight_NN.PNG",
    "Images_IG/Bishop_NB.PNG",
    "Images_IG/Queen_NN.PNG",
    "Images_IG/King_NB.PNG",
    "Images_IG/Bishop_NN.PNG",
    "Images_IG/Knight_NB.PNG",
    "Images_IG/Tower_NN.PNG",
]


global InitWhite
InitWhite = [
    "Images_IG/Tower_BN.PNG",
    "Images_IG/Knight_BB.PNG",
    "Images_IG/Bishop_BN.PNG",
    "Images_IG/Queen_BB.PNG",
    "Images_IG/King_BN.PNG",
    "Images_IG/Bishop_BB.PNG",
    "Images_IG/Knight_BN.PNG",
    "Images_IG/Tower_BB.PNG",
]

global InitAssocPieces
InitAssocPieces = [Tower, Knight, Bishop, Queen, King, Bishop, Knight, Tower]

global RealPiecesNames
RealPiecesNames = ["King", "Queen", "Tower", "Knight", "Bishop", "Pawn", "Pawn"]

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

global PiecesOrderBlackUp
PiecesOrderBlackUp = [Tower, Knight, Bishop, Queen, King, Bishop, Knight, Tower]

global PiecesOrderWhiteUp
PiecesOrderWhiteUp = [Tower, Knight, Bishop, King, Queen, Bishop, Knight, Tower]

global numberOfPiecesFEN
numberOfPiecesFEN = {
    "r": 2,
    "R": 2,
    "n": 2,
    "N": 2,
    "b": 2,
    "B": 2,
    "q": 1,
    "Q": 1,
    "k": 1,
    "K": 1,
    "p": 8,
    "P": 8,
}

global FEN_to_Piece
FEN_to_Piece = {
    "r": (Tower, 1),
    "R": (Tower, 2),
    "k": (King, 1),
    "K": (King, 2),
    "q": (Queen, 1),
    "Q": (Queen, 2),
    "n": (Knight, 1),
    "N": (Knight, 2),
    "b": (Bishop, 1),
    "B": (Bishop, 2),
    "p": (PawnL, 1),
    "P": (PawnR, 2),
}

global FEN_to_Pawn
FEN_to_Pawn = {
    ("p", 1): (PawnL, 1),
    ("p", 2): (PawnR, 1),
    ("P", 1): (PawnR, 2),
    ("P", 2): (PawnL, 2),
}

global Conv_Square_IA_to_IG
Conv_Square_IA_to_IG = {}
for i in range(8):
    for j in range(8):
        Conv_Square_IA_to_IG[i * 8 + j] = 63 - (i * 8 + j)

global Conv_Square_IG_to_IA
Conv_Square_IG_to_IA = {}
for i in range(8):
    for j in range(8):
        Conv_Square_IG_to_IA[Conv_Square_IA_to_IG[i * 8 + j]] = i * 8 + j


global KingC
KingC = 4

global QueenC
QueenC = 3

global TowerC
TowerC = 0

global KnightC
KnightC = 1

global BishopC
BishopC = 2

global PawnC
PawnC = 5

global Py_to_C
Py_to_C = {
    King: KingC,
    Queen: QueenC,
    Tower: TowerC,
    Knight: KnightC,
    Bishop: BishopC,
    PawnL: PawnC,
    PawnR: PawnC,
}

global C_to_Py
C_to_Py = {KingC: King, QueenC: Queen, TowerC: Tower, Knight: KnightC, BishopC: Bishop}


## Classes


class PersonnalButton(object):
    def __init__(self, Echiquier, i, j, Fen, isPawn=False):

        """
        Inputs :
            Echiquier : an Echiquier class object in which the button will be placed
            i,j : int representing the location of the button inside the Echiquier
            Fen : Ui_Play_Window associated. See report for more info
        Goal:
            Initialises the main fields of the button
        """

        # ---------------------------#
        #     Style Button Border   #
        # ---------------------------#
        self.buttonBorderAppear = "border-color : rgb(0,160,0);\n border-width : 3px; \n border-style : inset;"
        self.buttonBorderAppearCastle = "border-color : rgb(160,0,0);\n border-width : 3px; \n border-style : inset;"
        self.buttonBorderAppearIAMov = "border-color : rgb(0,192,255);\n border-width : 3px; \n border-style : inset;"
        self.buttonBorderDisappear = (
            "border-color : rgb(0,0,0);\n border-width : 0px; \n border-style : inset;"
        )

        self.fenetreAssoc = Fen
        self.pieceAssoc = None
        self.pawn = isPawn

        self.TabPromotion = np.empty(
            5, dtype=TakenButton
        )  # Will contain all buttons for promotion
        self.type = 0
        self.button = QtWidgets.QToolButton(Echiquier)
        self.button.setMaximumSize(QtCore.QSize(45, 45))
        self.location = np.array([i, j])
        self.icon1 = QtGui.QIcon()
        self.icon1.addPixmap(
            QtGui.QPixmap("Images_IG/Case_Blanche.PNG"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.icon2 = QtGui.QIcon()
        self.icon2.addPixmap(
            QtGui.QPixmap("Images_IG/Noir.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.button.clicked.connect(self.play_Button)

    def play_Button(self):

        """
        Goal :
            - Method that manage the selection of pieces and their deplacements.
            - Update of AI fields is included inside.
        """

        try:  # In case there is no associated piece on the clicked button
            if self.fenetreAssoc.selection:
                if self.fenetreAssoc.player == self.pieceAssoc.couleur:
                    for loc in self.fenetreAssoc.MovIA:
                        self.fenetreAssoc.Tab[loc[0], loc[1]].button.setStyleSheet(
                            self.buttonBorderDisappear
                        )
                    self.fenetreAssoc.MovIa = []
                    self.LightenPossibleDiplacements()

            elif self.fenetreAssoc.deplacement:

                ListPossibleDep, isCastle = self.fenetreAssoc.ListPossibleCase

                if tuple(self.location) in [tuple(pos) for pos in isCastle]:

                    self.fenetreAssoc.RedoPossible = False
                    self.fenetreAssoc.RedoList = []
                    self.DarkenDeplacements(ListPossibleDep, isCastle)
                    self.DeplacementForCastle()
                    self.fenetreAssoc.ListPossibleCase = [], []
                    self.fenetreAssoc.selection = True
                    self.fenetreAssoc.deplacement = False

                    # ----------------| AI fields |----------------#
                    pos_ini = (
                        8 * self.fenetreAssoc.caseSelec[0]
                        + self.fenetreAssoc.caseSelec[1]
                    )
                    pos_fin = 8 * self.location[0] + self.location[1]
                    prom = self.fenetreAssoc.DamierIA(pos_ini).Id

                    if self.fenetreAssoc.colorIA == 2:
                        pos_ini = Conv_Square_IG_to_IA[pos_ini]
                        pos_fin = Conv_Square_IG_to_IA[pos_fin]

                    # ----------------| AI move |----------------#
                    self.fenetreAssoc.DamierIA.bouge_piece(pos_ini, pos_fin, prom)

                elif tuple(self.location) in [tuple(pos) for pos in ListPossibleDep]:

                    # ----------------| AI fields |----------------#
                    pos_ini = (
                        8 * self.fenetreAssoc.caseSelec[0]
                        + self.fenetreAssoc.caseSelec[1]
                    )
                    pos_fin = 8 * self.location[0] + self.location[1]
                    prom = self.fenetreAssoc.DamierIA(pos_ini).Id  # no promotion yet

                    # ----------| Graphic Interface fields |----------#
                    self.DarkenDeplacements(ListPossibleDep, isCastle)
                    self.DeplacementNotCastle()
                    self.fenetreAssoc.ListPossibleCase = [], []
                    self.fenetreAssoc.selection = True
                    self.fenetreAssoc.deplacement = False
                    self.fenetreAssoc.RedoPossible = False
                    self.fenetreAssoc.RedoList = []

                    isProm = False

                    if self.fenetreAssoc.colorIA == 2:
                        pos_ini = Conv_Square_IG_to_IA[pos_ini]
                        pos_fin = Conv_Square_IG_to_IA[pos_fin]
                        prom = self.fenetreAssoc.DamierIA(pos_ini).Id

                    if (
                        self.pieceAssoc.piece == PawnR
                        and self.location[1 if self.fenetreAssoc.PVP else 0] == 0
                    ) or (
                        self.pieceAssoc.piece == PawnL
                        and self.location[1 if self.fenetreAssoc.PVP else 0] == 7
                    ):
                        self.Promotion(pos_ini, pos_fin)
                        isProm = True

                    # ----------------| AI move |----------------#
                    if not isProm:
                        # For move of AI when promotion occurs see TakenButton HandleButton method
                        self.fenetreAssoc.DamierIA.bouge_piece(pos_ini, pos_fin, prom)

                elif tuple(self.location) == tuple(self.fenetreAssoc.caseSelec):
                    pass

                else:
                    self.DarkenDeplacements(ListPossibleDep, isCastle)
                    self.fenetreAssoc.caseSelec = self.location
                    self.fenetreAssoc.ListPossibleCase = [], []
                    self.fenetreAssoc.selection = True
                    self.fenetreAssoc.deplacement = False

                    if (
                        self.pieceAssoc != None
                    ):  # Very crucial. Allows to immediatly replay.
                        self.play_Button()

        except AttributeError:
            pass  # In case there is no piece on the square. Totally normal

    def LightenPossibleDiplacements(self):

        """
        Method called when a case is selectionned.
        Goal :
            Lighten the possible deplacements in green or red
        """

        L, isCastle = self.pieceAssoc.PossibleDeplacement(self.pieceAssoc.piece == King)
        # Tests de la mise en échec (impossile de le mettre dans PossibleDeplacement vu que check appelle
        # possible deplacement (boucle infinie)
        LTrue = []
        formerloc = self.location
        formercolor = self.pieceAssoc.couleur
        for dep in L:
            pieceTaken = pld.DeplacementCopy(self.fenetreAssoc.Tab, formerloc, dep)
            if not pld.check(self.fenetreAssoc.Tab, self.fenetreAssoc.player):
                LTrue += [dep]
            pld.CancelMov(
                self.fenetreAssoc.Tab,
                self.fenetreAssoc.Damier,
                dep,
                formerloc,
                pieceTaken,
            )
        self.fenetreAssoc.ListPossibleCase = LTrue, isCastle
        for butt in [
            self.fenetreAssoc.Tab[k[0], k[1]]
            for k in self.fenetreAssoc.ListPossibleCase[0]
        ]:
            butt.button.setStyleSheet(self.buttonBorderAppear)
        for butt in [
            self.fenetreAssoc.Tab[k[0], k[1]]
            for k in self.fenetreAssoc.ListPossibleCase[1]
        ]:
            butt.button.setStyleSheet(self.buttonBorderAppearCastle)
        self.fenetreAssoc.selection = False
        self.fenetreAssoc.deplacement = True
        self.fenetreAssoc.caseSelec = self.location
        return None

    def DarkenDeplacements(self, ListPossibleDep, isCastle):

        """
        Method called when a deplacement is done
        Goal :
            Darken the previously lighten squares
        """

        for butt in [
            self.fenetreAssoc.Tab[k[0], k[1]] for k in ListPossibleDep + isCastle
        ]:
            # Il ne peut pas faire le List in List of List mais le tuple in List of Tuple marche
            butt.button.setStyleSheet(self.buttonBorderDisappear)
        return None

    def DeplacementForCastle(self):

        """
        Method called when a castle is being done
        Goals :
            - Deplace all pieces
            - Does NOT update AI
            - Update GI's fields
        """

        # ================ Forbidding Castles =================#
        if self.fenetreAssoc.player == 1:
            self.fenetreAssoc.Damier.CastleBGrand_Save = (
                self.fenetreAssoc.Damier.CastleBGrand
            )
            self.fenetreAssoc.Damier.CastleBSmall_Save = (
                self.fenetreAssoc.Damier.CastleBSmall
            )
            self.fenetreAssoc.Damier.CastleBGrand = False
            self.fenetreAssoc.Damier.CastleBSmall = False

        if self.fenetreAssoc.player == 2:
            self.fenetreAssoc.Damier.CastleWGrand_Save = (
                self.fenetreAssoc.Damier.CastleWGrand
            )
            self.fenetreAssoc.Damier.CastleWSmall_Save = (
                self.fenetreAssoc.Damier.CastleWSmall
            )
            self.fenetreAssoc.Damier.CastleWGrand = False
            self.fenetreAssoc.Damier.CastleWSmall = False

        # ================== Getting player ===================#

        self.fenetreAssoc.player_Save = (
            self.fenetreAssoc.player
        )  # saving current player
        self.fenetreAssoc.player = -1  # disabling all button before validation

        # =========== Getting locations of pieces =============#

        locationKingToMove = self.fenetreAssoc.caseSelec

        if self.fenetreAssoc.PVP:
            locationForTower = np.array(
                [
                    locationKingToMove[0] + (-1 if self.location[0] == 2 else 1),
                    self.location[1],
                ]
            )
            locationTowerToMove = np.array(
                [0 if self.location[0] == 2 else 7, locationKingToMove[1]]
            )

        elif self.fenetreAssoc.colorIA == 1:
            locationForTower = np.array(
                [
                    locationKingToMove[0],
                    self.location[1] + (1 if self.location[1] == 2 else -1),
                ]
            )
            locationTowerToMove = np.array(
                [locationKingToMove[0], 0 if self.location[1] == 2 else 7]
            )

        else:
            locationForTower = np.array(
                [
                    locationKingToMove[0],
                    self.location[1] + (1 if self.location[1] == 1 else -1),
                ]
            )
            locationTowerToMove = np.array(
                [locationKingToMove[0], 0 if self.location[1] == 1 else 7]
            )

        # ================== Getting piece to move ===================#
        PersButtToMove = self.fenetreAssoc.Tab[
            locationKingToMove[0], locationKingToMove[1]
        ]
        TowerToMove = self.fenetreAssoc.Tab[
            locationTowerToMove[0], locationTowerToMove[1]
        ]

        # ================== Registering Movement ====================#
        ListKing = [
            self.location,
            self.fenetreAssoc.caseSelec,
            None,
        ]  # Format : Loc , formerLoc, PieceTaken
        ListTower = [locationForTower, locationTowerToMove, None]
        self.fenetreAssoc.Mov = [ListKing, ListTower]

        # ================ Printing King at Location =================#
        name = (
            PiecesNames[King]
            + ("N" if PersButtToMove.pieceAssoc.couleur == 1 else "B")
            + ("N" if (self.location[0] + self.location[1]) % 2 == 1 else "B")
            + ".PNG"
        )
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(name), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button.setIcon(icon)

        # =============== Printing Tower at Location ==================#

        name = (
            PiecesNames[Tower]
            + ("N" if TowerToMove.pieceAssoc.couleur == 1 else "B")
            + ("N" if (self.location[0] + self.location[1]) % 2 == 0 else "B")
            + ".PNG"
        )  # == 0 because Tower is a case over or under the king
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(name), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.fenetreAssoc.Tab[locationForTower[0], locationForTower[1]].button.setIcon(
            icon
        )

        # ============== Removing from former location ===============#
        PersButtToMove.button.setIcon(
            self.fenetreAssoc.icon1
            if np.sum(PersButtToMove.location) % 2 == 0
            else self.fenetreAssoc.icon2
        )
        TowerToMove.button.setIcon(
            self.fenetreAssoc.icon1
            if np.sum(TowerToMove.location) % 2 == 0
            else self.fenetreAssoc.icon2
        )

        # ================== Updating ChessPlate ===================#
        self.pieceAssoc = Piece(
            self.fenetreAssoc.Damier,
            King,
            PersButtToMove.pieceAssoc.couleur,
            self.location,
            self.fenetreAssoc.Tab,
            self.fenetreAssoc.PVP,
        )
        self.fenetreAssoc.Tab[
            locationForTower[0], locationForTower[1]
        ].pieceAssoc = Piece(
            self.fenetreAssoc.Damier,
            Tower,
            TowerToMove.pieceAssoc.couleur,
            locationForTower,
            self.fenetreAssoc.Tab,
            self.fenetreAssoc.PVP,
        )
        self.fenetreAssoc.Damier.Dam[
            2 + PersButtToMove.location[0], 2 + PersButtToMove.location[1]
        ] = 0
        self.fenetreAssoc.Damier.Dam[
            2 + TowerToMove.location[0], 2 + TowerToMove.location[1]
        ] = 0
        self.fenetreAssoc.Damier.Dam[
            2 + self.location[0], 2 + self.location[1]
        ] = PersButtToMove.pieceAssoc.couleur
        self.fenetreAssoc.Damier.Dam[
            2 + locationForTower[0], 2 + locationForTower[1]
        ] = TowerToMove.pieceAssoc.couleur
        PersButtToMove.pieceAssoc = None
        self.fenetreAssoc.Tab[
            TowerToMove.location[0], TowerToMove.location[1]
        ].pieceAssoc = None

        # ============== Updating Fields (Selection/Deplacement) ==============#
        self.fenetreAssoc.ListPossibleCase = [], []
        self.fenetreAssoc.selection = True
        self.fenetreAssoc.deplacement = False
        self.fenetreAssoc.numberOfHalfMoveSave = self.fenetreAssoc.numberOfHalfMove
        self.fenetreAssoc.numberOfHalfMove += 1
        self.fenetreAssoc.numberOfMove += self.fenetreAssoc.player_Save == 2

        return None

    def DeplacementNotCastle(self):

        """
        Method called when a move which is not a castle is being done
        Goals :
            - Deplace all pieces
            - Does NOT update AI
            - Update GI's fields
        """

        # ================== Getting Taken Piece ==================#

        PieceMoved = self.pieceAssoc
        self.AddTakenPiece(PieceMoved)

        # ================== Getting player ===================#

        self.fenetreAssoc.player_Save = (
            self.fenetreAssoc.player
        )  # saving current player
        self.fenetreAssoc.player = -1  # disabling all button before validation

        # ================== Getting piece to move ===================#
        locationPieceToMove = self.fenetreAssoc.caseSelec
        PersButtToMove = self.fenetreAssoc.Tab[
            locationPieceToMove[0], locationPieceToMove[1]
        ]

        # ================== Updating Possibles Castles ===================#
        if PersButtToMove.pieceAssoc.piece == King:
            if self.fenetreAssoc.player_Save == 1:
                self.fenetreAssoc.Damier.CastleBGrand_Save = (
                    self.fenetreAssoc.Damier.CastleBGrand
                )
                self.fenetreAssoc.Damier.CastleBSmall_Save = (
                    self.fenetreAssoc.Damier.CastleBSmall
                )
                self.fenetreAssoc.Damier.CastleBGrand = False
                self.fenetreAssoc.Damier.CastleBSmall = False

            if self.fenetreAssoc.player_Save == 2:
                self.fenetreAssoc.Damier.CastleWGrand_Save = (
                    self.fenetreAssoc.Damier.CastleWGrand
                )
                self.fenetreAssoc.Damier.CastleWSmall_Save = (
                    self.fenetreAssoc.Damier.CastleWSmall
                )
                self.fenetreAssoc.Damier.CastleWGrand = False
                self.fenetreAssoc.Damier.CastleWSmall = False

        elif PersButtToMove.pieceAssoc.piece == Tower:
            iking, jking = pld.FindKing(
                self.fenetreAssoc.Tab, self.fenetreAssoc.player_Save
            )
            dist2D = np.abs(PersButtToMove.location - np.array([iking, jking]))

            if self.fenetreAssoc.PVP:
                cont = (dist2D[1] == 0) and (PersButtToMove.location[0] in [0, 7])
                dist = dist2D[0]
                # meaning that king and Tower are on the same line and tower is
                # at one of the extremities
            else:
                cont = (dist2D[0] == 0) and (PersButtToMove.location[1] in [0, 7])
                dist = dist2D[1]
                # meaning that king and Tower are on the same column and tower
                # is at one of the extremities

            if self.fenetreAssoc.player_Save == 1 and cont:
                if dist == 4:
                    self.fenetreAssoc.Damier.CastleBGrand_Save = (
                        self.fenetreAssoc.Damier.CastleBGrand
                    )
                    self.fenetreAssoc.Damier.CastleBGrand = False
                else:
                    self.fenetreAssoc.Damier.CastleBSmall_Save = (
                        self.fenetreAssoc.Damier.CastleBSmall
                    )
                    self.fenetreAssoc.Damier.CastleBSmall = False

            if self.fenetreAssoc.player_Save == 2 and cont:
                if dist == 4:
                    self.fenetreAssoc.Damier.CastleWGrand_Save = (
                        self.fenetreAssoc.Damier.CastleWGrand
                    )
                    self.fenetreAssoc.Damier.CastleWGrand = False
                else:
                    self.fenetreAssoc.Damier.CastleWSmall_Save = (
                        self.fenetreAssoc.Damier.CastleWSmall
                    )
                    self.fenetreAssoc.Damier.CastleWSmall = False

        # ================== Registering Movement ====================#
        self.fenetreAssoc.Mov = [
            [self.location, self.fenetreAssoc.caseSelec, self.pieceAssoc],
            [],
        ]  # Format : loc, formerLoc, pieceTaken
        self.fenetreAssoc.numberOfMove += self.fenetreAssoc.player_Save == 2

        self.fenetreAssoc.numberOfHalfMoveSave = self.fenetreAssoc.numberOfHalfMove
        if self.pieceAssoc == None:
            self.fenetreAssoc.numberOfHalfMove = 1 + self.fenetreAssoc.numberOfHalfMove
        else:
            self.fenetreAssoc.numberOfHalfMove = 0

        # ================== Printing at location ====================#
        name = (
            PiecesNames[PersButtToMove.pieceAssoc.piece]
            + ("N" if PersButtToMove.pieceAssoc.couleur == 1 else "B")
            + ("N" if (self.location[0] + self.location[1]) % 2 == 1 else "B")
            + ".PNG"
        )
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(name), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button.setIcon(icon)

        # ============== Removing from former location ===============#
        PersButtToMove.button.setIcon(
            self.fenetreAssoc.icon1
            if np.sum(PersButtToMove.location) % 2 == 0
            else self.fenetreAssoc.icon2
        )

        # ================== Updating ChessPlate ===================#
        self.pieceAssoc = Piece(
            self.fenetreAssoc.Damier,
            PersButtToMove.pieceAssoc.piece,
            PersButtToMove.pieceAssoc.couleur,
            self.location,
            self.fenetreAssoc.Tab,
            self.fenetreAssoc.PVP,
        )
        self.fenetreAssoc.Damier.Dam[
            2 + PersButtToMove.location[0], 2 + PersButtToMove.location[1]
        ] = 0
        self.fenetreAssoc.Damier.Dam[
            2 + self.location[0], 2 + self.location[1]
        ] = PersButtToMove.pieceAssoc.couleur
        PersButtToMove.pieceAssoc = None

        # ================== Pawns Extension Upd ===================#
        if self.pieceAssoc.piece == PawnL:
            extSupp = (self.pieceAssoc.PVP and self.location[1] == 1) or (
                not self.pieceAssoc.PVP and self.location[0] == 1
            )
            self.pieceAssoc.finExt = 2 + extSupp

        elif self.pieceAssoc.piece == PawnR:
            extSupp = (self.pieceAssoc.PVP and self.location[1] == 6) or (
                not self.pieceAssoc.PVP and self.location[0] == 6
            )
            self.pieceAssoc.finExt = 2 + extSupp

        # ============== Updating Fields (Selection/Deplacement) ==============#
        self.fenetreAssoc.ListPossibleCase = [], []
        self.fenetreAssoc.selection = True
        self.fenetreAssoc.deplacement = False

        return None

    def AddTakenPiece(self, PieceMoved):

        """
        Method called when a piece is taken during a move
        Inputs :
            self
            PieceMoved : Piece Object or None. If None, does nothing
        Goal :
            Add the pieceMoved to the corresponding list of taken pieces in the GI
        """

        if PieceMoved != None:
            nameAddedPiece = (
                PiecesNames[PieceMoved.piece]
                + ("N" if PieceMoved.couleur == 1 else "B")
                + ".PNG"
            )
            iconAddedPiece = QtGui.QIcon()
            iconAddedPiece.addPixmap(
                QtGui.QPixmap(nameAddedPiece), QtGui.QIcon.Normal, QtGui.QIcon.Off
            )
            item = QtWidgets.QListWidgetItem()
            item.setText(RealPiecesNames[PieceMoved.piece])
            font = QtGui.QFont()
            font.setFamily("Rockwell")
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            item.setFont(font)
            item.setForeground(QtGui.QColor(255, 255, 255))
            item.setIcon(iconAddedPiece)
            if PieceMoved.couleur == 1:
                self.fenetreAssoc.listWidget_2.addItem(item)
            else:
                self.fenetreAssoc.listWidget.addItem(item)

    def RemoveTakenPiece(self, col):

        """
        Method called when a taken piece returns to the board
        Inputs :
            col : int \in {1,2}
        Goal :
            Delete the last piece in the given @param col with @param col = 1 for black pieces and 2 for white pieces
        """

        if col == 1:
            self.fenetreAssoc.listWidget.takeItem(
                self.fenetreAssoc.listWidget.count() - 1
            )
        if col == 2:
            self.fenetreAssoc.listWidget_2.takeItem(
                self.fenetreAssoc.listWidget_2.count() - 1
            )

    def Promotion(self, pos_ini, pos_fin):

        """
        Method called for a player promotion
        Inputs :
            pos_ini, pos_fin : 2 int representing the former and the new location of the piece according to AI convention (from 0n to 63)
        Goal :
            Handles everything from the creation of buttons to the update of all AI and GI fields.
        """

        # ---------------| Widget itself |--------------#
        widgetPromotion = QtWidgets.QWidget(self.fenetreAssoc.MainWindow)
        widgetPromotion.setObjectName("widgetPromotion")
        gridLayout = QtWidgets.QGridLayout(widgetPromotion)

        # ---------------| Pieces Button |--------------#
        for i in range(1, 5):
            self.TabPromotion[i - 1] = TakenButton(
                i,
                self.pieceAssoc.couleur,
                self.fenetreAssoc,
                self.location,
                widgetPromotion,
                pos_ini,
                pos_fin,
            )
            gridLayout.addWidget(self.TabPromotion[i - 1].butt, 0, i, 1, 1)

        # ---------------| Indication |--------------#
        indicLabel = QtWidgets.QLabel(widgetPromotion)
        font = QtGui.QFont()
        font.setFamily("Rockwell")
        font.setPointSize(11)
        indicLabel.setFont(font)
        indicLabel.setAlignment(QtCore.Qt.AlignCenter)
        indicLabel.setText("Choose which piece you want to promote.")
        gridLayout.addWidget(indicLabel, 1, 1, 1, 4)
        gridLayout.setHorizontalSpacing(34)
        self.fenetreAssoc.TopLayout.addWidget(widgetPromotion, 4, 2, 1, 1)
        self.fenetreAssoc.PromotionInProgress = True
        self.fenetreAssoc.Undo.setEnabled(False)
        self.fenetreAssoc.Redo.setEnabled(False)
        self.fenetreAssoc.Validate.setEnabled(False)

    def resizeEvent(self, event):

        """
        Method automatically called when the buttons are being resized
        """

        new_size_square = (
            min(
                self.fenetreAssoc.MainWindow.width(),
                self.fenetreAssoc.MainWindow.height(),
            )
            * 45
            / 800
        )
        self.button.setMaximumSize(new_size_square, new_size_square)
        self.button.resize(event.size())


class TakenButton(object):
    """
    Class of buttons allowing to handle the player promotion from PersonnalButton.Promotion. Please do not use that class except for that function.
    """

    def __init__(self, piece, col, win, location, parentWidget, pos_ini, pos_fin):
        self.piece = piece
        self.color = col
        self.windowAssoc = win
        self.location = location
        self.posIA = [pos_ini, pos_fin]
        self.parent = parentWidget

        self.butt = QtWidgets.QToolButton(parentWidget)
        self.butt.setMaximumSize(QtCore.QSize(45, 45))
        self.butt.setStyleSheet("background-color : rgb(255,208,128)")
        self.name = PiecesNames[self.piece] + ("N" if self.color == 1 else "B")
        icon = QtGui.QIcon()
        self.butt.setIconSize(QtCore.QSize(200, 200))
        icon.addPixmap(
            QtGui.QPixmap(self.name + ".PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.butt.setIcon(icon)

        self.butt.clicked.connect(self.handleButton)

    def handleButton(self):
        self.windowAssoc.Tab[self.location[0], self.location[1]].pieceAssoc = Piece(
            self.windowAssoc.Damier,
            self.piece,
            self.color,
            self.location,
            self.windowAssoc.Tab,
            self.windowAssoc.PVP,
        )
        name = self.name + ("N" if (np.sum(self.location)) % 2 == 1 else "B") + ".PNG"
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(name), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.windowAssoc.Tab[self.location[0], self.location[1]].button.setIcon(icon)
        self.handleClose()
        return None

    def handleClose(self):
        self.parent.hide()
        prom = Py_to_C[self.piece]
        self.windowAssoc.DamierIA.bouge_piece(self.posIA[0], self.posIA[1], prom)
        self.windowAssoc.ValidateAction()

    def resizeEvent(self):
        new_size_square = (
            min(self.winAssoc.MainWindow.width(), self.winAssoc.MainWindow.height())
            * 45
            / 800
        )
        self.button.setMaximumSize(new_size_square, new_size_square)
        self.button.resize(event.size())


class Echiquier(PersonnalButton):
    """
    Class representing the echiquier and containing all the associated personnal buttons
    """

    def __init__(self, parent, Fen):
        """
        Init method
        Inputs :
            parent : QWidget in which the Echiquier will be inserted.
            Fen : Ui_PlayWindow the echiquier is going to be linked to
        """
        self.Echiquier = QtWidgets.QWidget(parent)

        self.Echiquier.setObjectName("Echiquier")
        self.gridLayout = QtWidgets.QGridLayout(self.Echiquier)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.Echiquier.setStyleSheet("background-image : url(Images_IG/Bord.jpg)")

        # ---------------------------#
        #       Icons DownLoad      #
        # ---------------------------#

        self.icon1 = QtGui.QIcon()
        self.icon1.addPixmap(
            QtGui.QPixmap("Images_IG/Case_Blanche.PNG"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.icon2 = QtGui.QIcon()
        self.icon2.addPixmap(
            QtGui.QPixmap("Images_IG/Noir.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )

        # ---------------------------#
        #       Creating Boxes      #
        # ---------------------------#

        self.Tab = np.empty((8, 8), dtype=PersonnalButton)  # Will contain all buttons
        for i in range(8):
            for j in range(8):
                self.Tab[i, j] = PersonnalButton(self.Echiquier, i, j, Fen)

        # Echiquier

        nameL = ["A", "B", "C", "D", "E", "F", "G", "H"]  # Boxes' Names

        # ---------------------------#
        #       Filling Boxes       #
        # ---------------------------#

        for i in range(8):
            for j in range(8):
                self.Tab[i, j].button.setAutoFillBackground(True)
                self.Tab[i, j].button.setText("")
                if (i + j) % 2 == 0:
                    self.Tab[i, j].button.setIcon(self.icon1)
                else:
                    self.Tab[i, j].button.setIcon(self.icon2)
                self.Tab[i, j].button.setIconSize(QtCore.QSize(250, 250))
                self.Tab[i, j].button.setObjectName(nameL[i] + str(j + 1))
                self.gridLayout.addWidget(self.Tab[i, j].button, i + 1, j + 1, 1, 1)

        # ---------------------------#
        #    Creating Boundaries    #
        # ---------------------------#

        self.Ex_D_H = QtWidgets.QLabel(self.Echiquier)
        self.Ex_D_H.setMaximumSize(QtCore.QSize(25, self.Tab[0, 0].button.width() * 8))
        self.Ex_D_H.setAutoFillBackground(False)
        self.Ex_D_H.setText("")
        self.Ex_D_H.setPixmap(QtGui.QPixmap("Images_IG/Bord.jpg"))
        self.Ex_D_H.setScaledContents(True)
        self.Ex_D_H.setObjectName("Ex_D_H")
        self.gridLayout.addWidget(self.Ex_D_H, 1, 9, 8, 1)
        self.Ex_G_H = QtWidgets.QLabel(self.Echiquier)
        self.Ex_G_H.setMaximumSize(
            QtCore.QSize(self.Tab[0, 0].button.width() * 8 + 2 * 35, 25)
        )
        self.Ex_G_H.setAutoFillBackground(False)
        self.Ex_G_H.setText("")
        self.Ex_G_H.setPixmap(QtGui.QPixmap("Images_IG/Bord.jpg"))
        self.Ex_G_H.setScaledContents(True)
        self.Ex_G_H.setObjectName("Ex_G_H")
        self.gridLayout.addWidget(self.Ex_G_H, 0, 0, 1, 10)

        self.Ex_D_B = QtWidgets.QLabel(self.Echiquier)
        self.Ex_D_B.setMaximumSize(
            QtCore.QSize(self.Tab[0, 0].button.width() * 8 + 2 * 35, 25)
        )
        self.Ex_D_B.setAutoFillBackground(False)
        self.Ex_D_B.setText("")
        self.Ex_D_B.setPixmap(QtGui.QPixmap("Images_IG/Bord.jpg"))
        self.Ex_D_B.setScaledContents(True)
        self.Ex_D_B.setObjectName("Ex_D_B")
        self.gridLayout.addWidget(self.Ex_D_B, 9, 0, 1, 10)
        self.Ex_G_B_2 = QtWidgets.QLabel(self.Echiquier)
        self.Ex_G_B_2.setMaximumSize(
            QtCore.QSize(25, self.Tab[0, 0].button.width() * 8)
        )
        self.Ex_G_B_2.setAutoFillBackground(False)
        self.Ex_G_B_2.setText("")
        self.Ex_G_B_2.setPixmap(QtGui.QPixmap("Images_IG/Bord.jpg"))
        self.Ex_G_B_2.setScaledContents(True)
        self.Ex_G_B_2.setObjectName("Ex_G_B_2")
        self.gridLayout.addWidget(self.Ex_G_B_2, 1, 0, 8, 1)

    def resizeEvent(self, event):
        """
        Automatic resize method.
        Goal :
            Keep the echiquier square when enlarging the associated window.
        """
        for i in range(8):
            for j in range(8):
                self.Tab[i, j].resizeEvent(event)
        self.Ex_D_H.setMaximumSize(QtCore.QSize(25, self.Tab[0, 0].button.width() * 8))
        self.Ex_D_B.setMaximumSize(
            QtCore.QSize(self.Tab[0, 0].button.width() * 8 + 2 * 35, 25)
        )
        self.Ex_G_H.setMaximumSize(
            QtCore.QSize(self.Tab[0, 0].button.width() * 8 + 2 * 35, 25)
        )
        self.Ex_G_B_2.setMaximumSize(
            QtCore.QSize(25, self.Tab[0, 0].button.width() * 8)
        )


class Ui_PlayWindow(object):
    """
    Uppest level of the graphical interface
    Manage everything that is linked to the graphic interface
    """

    def __init__(
        self, MainWindow, PVP, IW, nameP1, nameP2=None, colorAI=None, FEN=None
    ):
        """
        Init Method
        Inputs :
            MainWindow : QMainWindow in which the Play Window is put
            PVP : bool. If true then Player VS Player mode is on otherwise it is
                        AI mode that is activated.
            IW : Ui_MainWindow object from Initial_Window.py
            nameP1 : str, name of first player
        Kwargs :
                    ATTENTION : one of the two following args mus be
                    specified.
            nameP2 : str, second name if PVP mode
            colorIA : int, represents color of IA (1 = Black, 2 = White)
            FEN : str, FEN format, if != None, initializes the chessboard and
                  evrything related. To learn more click on the following link :
                  https://www.iechecs.com/notation.htm
        Goal :
            Initialises main field of the game.

        """

        # ---------------------------#
        #   Link to Initial Window  #
        # ---------------------------#
        self.IW = IW
        self.FEN = FEN

        # ---------------------------#
        #         AI Fields         #
        # ---------------------------#
        self.PVP = PVP
        self.DamierIA = p11m.Damier()
        self.colorIA = 1 if colorAI == None else colorAI
        self.fakeColorIA = self.colorIA if colorAI != 2 else 1
        self.MovIA = []
        self.difficultyAI = 5

        # ---------------------------#
        #        Name Fields        #
        # ---------------------------#
        if self.PVP:
            self.textW = nameP1
            self.textB = nameP2

        else:
            self.textW = nameP1 if self.colorIA == 1 else "AI"
            self.textB = nameP1 if self.colorIA == 2 else "AI"

        # ---------------------------#
        #        Rules Load         #
        # ---------------------------#

        f = open("Text/Rules.txt", "r")
        self.RulesString = ""
        RulesList = f.readlines()
        for ligneStr in RulesList:
            self.RulesString += ligneStr
        f.close()

        # ---------------------------#
        #       Filling Window      #
        # ---------------------------#
        self.MainWindow = MainWindow
        # self.MainWindow.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.MainWindow.resize(923, 780)
        iconExe = QtGui.QIcon("Images_IG/IconExe2.ico")
        self.MainWindow.setWindowIcon(iconExe)
        self.MainWindow.setStyleSheet("background-color: rgb(255, 255, 222);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # ---------------------------#
        #     Intializing Layouts   #
        # ---------------------------#

        # Top - Central - Verticals
        self.TopLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.TopLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.TopLayout.setObjectName("TopLayout")

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")

        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        # Grid englobing the Echiquier (With VideLabels)
        self.Echiquier_Spacer = QtWidgets.QWidget(self.centralwidget)
        self.Echiquier_Spacer.setObjectName("Echiquier_Spacer")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.Echiquier_Spacer)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.Echiquier = Echiquier(self.Echiquier_Spacer, self)
        self.Tab = self.Echiquier.Tab
        # Tab représente ainsi l'échiquier sous forme de boutons avec l'origine en haut à gauche. Pour accéder au bouton lettre numero (type A4) il faut faire Tab[numero][numero de la lettre] car les abscisses sont les num et les ordonnées les lettres

        # ---------------------------#
        #      Creating Palette     #
        # ---------------------------#

        self.palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(195, 195, 195))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)

        # ---------------------------#
        #       Icons DownLoad      #
        # ---------------------------#

        self.icon1 = QtGui.QIcon()
        self.icon1.addPixmap(
            QtGui.QPixmap("Images_IG/Case_Blanche.PNG"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.icon2 = QtGui.QIcon()
        self.icon2.addPixmap(
            QtGui.QPixmap("Images_IG/Noir.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )

        # ---------------------------#
        #     Creating Menu bar     #
        # ---------------------------#

        self.font = QtGui.QFont()
        self.font.setFamily("Rockwell")
        self.font.setPointSize(11)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setFixedHeight(26)
        self.menubar.setFont(self.font)
        self.menubar.setStyleSheet(
            "background-color : rgb(120,0,0); color : rgb(195,195,195)"
        )
        self.menubar.setObjectName("menubar")
        self.menuWindow = QtWidgets.QMenu(self.menubar)
        self.menuWindow.setObjectName("menuWindow")
        self.showIW = QtWidgets.QAction(
            QtGui.QIcon("Images_IG/OpenIcon.png"), "Open Menu Window", self.MainWindow
        )
        self.showIW.setObjectName("showIW")
        self.showIW.triggered.connect(self.IW.MainWindow.show)
        self.menuWindow.addAction(self.showIW)
        self.hideIW = QtWidgets.QAction(
            QtGui.QIcon("Images_IG/CloseIcon.png"), "Close Menu Window", self.MainWindow
        )
        self.hideIW.setObjectName("hideIW")
        self.hideIW.triggered.connect(self.IW.MainWindow.hide)
        self.menuWindow.addAction(self.hideIW)

        self.menuGame = QtWidgets.QMenu(self.menubar)
        self.menuGame.setObjectName("menuGame")
        self.MainWindow.setMenuBar(self.menubar)
        self.endGame = QtWidgets.QAction(
            QtGui.QIcon("Images_IG/CloseIcon.png"), "Stop Game", self.MainWindow
        )
        self.endGame.setObjectName("endGame")
        self.endGame.triggered.connect(self.CloseAction)
        self.menuGame.addAction(self.endGame)
        self.Rules = QtWidgets.QAction(
            QtGui.QIcon("Images_IG/Rules.png"),
            "Rules and fonctionalities",
            self.MainWindow,
        )
        self.Rules.setObjectName("Rules")
        self.Rules.triggered.connect(self.openRules)
        self.menuGame.addAction(self.Rules)
        self.saveGame = QtWidgets.QAction(
            QtGui.QIcon("Images_IG/SaveIcon.png"), "Save Game", self.MainWindow
        )
        self.saveGame.triggered.connect(self.SaveAction)
        self.saveGame.setObjectName("saveGame")
        self.menuGame.addAction(self.saveGame)
        self.openGame = QtWidgets.QAction(
            QtGui.QIcon("Images_IG/OpenGameIcon.png"),
            "Open a saved game",
            self.MainWindow,
        )
        self.openGame.setObjectName("openGame")
        self.openGame.triggered.connect(self.OpenAction)
        self.menuGame.addAction(self.openGame)

        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.MainWindow.setMenuBar(self.menubar)
        self.manageFile = QtWidgets.QAction(
            QtGui.QIcon("Images_IG/DeleteIcon.png"),
            "Manage your game files",
            self.MainWindow,
        )
        self.manageFile.setObjectName("manageFile")
        self.manageFile.triggered.connect(self.handle_File)
        self.menuFile.addAction(self.manageFile)

        self.menuAI = QtWidgets.QMenu(self.menubar)
        self.menuAI.setObjectName("menuAI")
        self.manageAI = QtWidgets.QAction(
            QtGui.QIcon("Images_IG/AIIcon.png"), "Manage AI Level", self.MainWindow
        )
        self.manageAI.setObjectName("manageAI")
        self.manageAI.triggered.connect(self.levelIA)
        self.menuAI.addAction(self.manageAI)

        self.menubar.addAction(self.menuWindow.menuAction())
        self.menubar.addAction(self.menuGame.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAI.menuAction())

        # ---------------------------#
        #       Playing Fields      #
        # ---------------------------#

        self.selection = True
        self.deplacement = False
        self.casePossible = []
        self.Damier = Damier(self.PVP, self.icon1, self.icon2)
        self.player = 2
        self.player_Save = -1
        self.RedoPossible = False
        self.numberOfMove = 1
        self.numberOfHalfMove = 0
        self.numberOfHalfMoveSave = 0
        self.PromotionInProgress = False

    def setupUi(self):
        """
        Complement to __ini__
        Please always call that one after __ini__. It allows to
        create and fill all the buttons and lists.
        """

        # ---------------------------------------------------------#
        # Vertical Layout for Black Player (Taken pieces, Points) #
        # ---------------------------------------------------------#

        self.FWP = QtWidgets.QLabel(self.centralwidget)
        self.FWP.setMaximumSize(QtCore.QSize(215, 16777215))
        self.FWP.setPalette(self.palette)

        self.FWP.setFont(self.font)
        self.FWP.setStyleSheet("background-color: rgb(120, 0, 0);")
        self.FWP.setAlignment(QtCore.Qt.AlignCenter)
        self.FWP.setObjectName("label")
        self.verticalLayout.addWidget(self.FWP)
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setMaximumSize(QtCore.QSize(215, 16777215))
        self.listWidget.setStyleSheet("background-color: rgb(85, 0, 0);")
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setIconSize(QtCore.QSize(40, 40))
        self.verticalLayout.addWidget(self.listWidget)
        self.BPP = QtWidgets.QLabel(self.centralwidget)
        self.BPP.setMaximumSize(QtCore.QSize(215, 16777215))
        self.BPP.setPalette(self.palette)
        self.BPP.setFont(self.font)
        self.BPP.setStyleSheet("background-color: rgb(120, 0, 0);")
        self.BPP.setAlignment(QtCore.Qt.AlignCenter)
        self.BPP.setObjectName("label_2")
        self.verticalLayout.addWidget(self.BPP)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 17)
        self.verticalLayout.setStretch(2, 1)
        self.TopLayout.addLayout(
            self.verticalLayout, 0, 0, 5, 1
        )  # Adding vertical Layout inside TopLayout

        # ---------------------------------------------------------#
        # Vertical Layout for White Player (Taken pieces, Points) #
        # ---------------------------------------------------------#

        self.FBP = QtWidgets.QLabel(self.centralwidget)
        self.FBP.setMaximumSize(QtCore.QSize(214, 16777215))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(195, 195, 195))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        self.FBP.setPalette(self.palette)
        self.FBP.setFont(self.font)
        self.FBP.setStyleSheet("background-color: rgb(120, 0, 0);")
        self.FBP.setAlignment(QtCore.Qt.AlignCenter)
        self.FBP.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.FBP)
        self.listWidget_2 = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_2.setMaximumSize(QtCore.QSize(214, 16777215))
        self.listWidget_2.setStyleSheet("background-color: rgb(85, 0, 0);")
        self.listWidget_2.setObjectName("listWidget_2")
        self.listWidget_2.setIconSize(QtCore.QSize(40, 40))
        self.verticalLayout_2.addWidget(self.listWidget_2)
        self.WPP = QtWidgets.QLabel(self.centralwidget)
        self.WPP.setMaximumSize(QtCore.QSize(214, 16777215))
        self.WPP.setPalette(self.palette)
        self.WPP.setFont(self.font)
        self.WPP.setStyleSheet("background-color: rgb(120, 0, 0);")
        self.WPP.setAlignment(QtCore.Qt.AlignCenter)
        self.WPP.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.WPP)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 17)
        self.verticalLayout_2.setStretch(2, 1)
        self.TopLayout.addLayout(
            self.verticalLayout_2, 0, 4, 5, 1
        )  # Adding vertical Layout inside TopLayout

        # ----------------------------#
        #   Setting the Echiquier    #
        # ----------------------------#

        self.gridLayout_2.addWidget(self.Echiquier.Echiquier, 1, 0, 1, 1)

        # -----------------------------#
        #       Englobing Grid        #
        # -----------------------------#

        spacerItem = QtWidgets.QSpacerItem(
            30, 16777215, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.gridLayout_2.addItem(spacerItem, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(
            30, 16777215, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.gridLayout_2.addItem(spacerItem1, 2, 0, 1, 1)
        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout_2.setRowStretch(0, 1)
        self.TopLayout.addWidget(self.Echiquier_Spacer, 2, 2, 1, 1)

        # ---------------------------#
        #       Creating Title      #
        # ---------------------------#

        self.PontsChess = QtWidgets.QLabel(self.centralwidget)
        self.PontsChess.setMaximumHeight(90)
        font = QtGui.QFont()
        font.setFamily("Rockwell")
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.PontsChess.setFont(font)
        self.PontsChess.setStyleSheet(
            "border-color: rgb(0, 0, 0);\n"
            "background-color: qlineargradient(spread:pad, x1:0.498, y1:0, x2:0.507249, y2:1, stop:0 rgba(145, 0, 0, 255), stop:0.855721 rgba(97, 0, 0, 255));"
        )
        self.PontsChess.setAlignment(QtCore.Qt.AlignCenter)
        self.PontsChess.setObjectName("PontsChess")
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(195, 195, 195))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        self.PontsChess.setPalette(self.palette)
        self.TopLayout.addWidget(self.PontsChess, 0, 1, 1, 3)

        self.Winning = QtWidgets.QLabel(self.centralwidget)
        self.Winning.setText("")
        self.Winning.setObjectName("Winning")
        self.TopLayout.addWidget(self.Winning, 4, 1, 1, 3)

        # ----------------------------#
        # Creating Validation Widget #
        # ----------------------------#

        self.widgetValidation = QtWidgets.QWidget(self.MainWindow)
        self.widgetValidation.setObjectName("widgetValidation")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widgetValidation)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # ---------------| Undo |--------------#
        self.Undo = QtWidgets.QToolButton(self.widgetValidation)
        self.Undo.setMaximumSize(QtCore.QSize(75, 45))
        self.Undo.setAutoFillBackground(True)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap("Images_IG/retour_arriere.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.Undo.setIcon(icon)
        self.Undo.setIconSize(QtCore.QSize(75, 45))
        self.Undo.setObjectName("Undo")
        self.horizontalLayout.addWidget(self.Undo)
        self.Undo.clicked.connect(self.UndoAction)

        # ---------------| Validate |---------------#
        self.Validate = QtWidgets.QToolButton(self.widgetValidation)
        self.Validate.setMaximumSize(QtCore.QSize(45, 45))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap("Images_IG/bouton_valider.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.Validate.setIcon(icon1)
        self.Validate.setIconSize(QtCore.QSize(90, 90))
        self.Validate.setObjectName("Validate")
        self.horizontalLayout.addWidget(self.Validate)
        self.Validate.clicked.connect(self.ValidateAction)

        # ---------------| Redo |--------------#
        self.Redo = QtWidgets.QToolButton(self.widgetValidation)
        self.Redo.setMaximumSize(QtCore.QSize(75, 45))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(
            QtGui.QPixmap("Images_IG/retour_avant.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.Redo.setIcon(icon2)
        self.Redo.setIconSize(QtCore.QSize(75, 45))
        self.Redo.setObjectName("Redo")
        self.horizontalLayout.addWidget(self.Redo)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 1)
        self.Redo.clicked.connect(self.RedoAction)
        self.TopLayout.addWidget(self.widgetValidation, 3, 2, 1, 1)

        # ----------------------------#
        #   Creating Rules widgets   #
        # ----------------------------#

        self.widgetRules = QtWidgets.QWidget(self.MainWindow)
        self.widgetRules.setObjectName("widgetRules")
        self.gridLayoutRules = QtWidgets.QGridLayout(self.widgetRules)
        self.gridLayoutRules.setObjectName("gridLayoutRules")

        self.RulesText = QtWidgets.QTextEdit(self.widgetRules)
        self.RulesText.setReadOnly(True)
        self.RulesText.setFont(self.font)
        self.RulesText.append(self.RulesString)

        urlLink = '<a href="https://en.wikipedia.org/wiki/Rules_of_chess">Rules</a>'
        self.labelLink = QtWidgets.QLabel(self.widgetRules)
        self.labelLink.setText(urlLink)
        self.labelLink.setAlignment(QtCore.Qt.AlignCenter)
        self.labelLink.setOpenExternalLinks(True)
        self.labelLink.setFont(self.font)

        self.CloseRulesButton = QtWidgets.QToolButton(self.widgetRules)
        self.CloseRulesButton.setStyleSheet("background-color : rgb(185,0,0)")
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap("Images_IG/CloseIcon.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.CloseRulesButton.setIcon(icon)
        self.CloseRulesButton.setMinimumSize(QtCore.QSize(50, 35))
        self.CloseRulesButton.clicked.connect(self.closeRules)

        self.gridLayoutRules.addWidget(self.RulesText, 0, 0, 6, 3)
        self.gridLayoutRules.addWidget(self.labelLink, 0, 3, 1, 1)
        self.gridLayoutRules.addWidget(self.CloseRulesButton, 3, 3, 1, 1)
        self.TopLayout.addWidget(self.widgetRules, 3, 1, 3, 3)
        self.widgetRules.hide()

        # ===============================================
        font = QtGui.QFont()
        font.setFamily("Rockwell")
        font.setPointSize(11)
        self.VideLabel1 = QtWidgets.QLabel(self.centralwidget)
        self.VideLabel1.setFont(font)
        self.VideLabel1.setAlignment(QtCore.Qt.AlignCenter)
        self.VideLabel1.setText("-")
        self.VideLabel1.setObjectName("VideLabel1")
        self.TopLayout.addWidget(self.VideLabel1, 1, 1, 1, 3)
        self.TopLayout.setRowStretch(0, 2)
        self.TopLayout.setRowStretch(1, 1)
        self.TopLayout.setRowStretch(2, 5)
        self.TopLayout.setRowStretch(3, 1)
        self.TopLayout.setRowStretch(4, 1)
        self.TopLayout.setColumnStretch(0, 1)
        self.TopLayout.setColumnStretch(1, 1)
        self.TopLayout.setColumnStretch(2, 1)
        self.TopLayout.setColumnStretch(3, 1)
        self.TopLayout.setColumnStretch(4, 1)
        self.MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(self.MainWindow)
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

        # ------------------| Initialisation of Game |------------------#
        self.Initialisation(self.FEN)

    def retranslateUi(self, MainWindow):
        """
        Method called in setupUI
        Goal :
            Gives a name to all menus and windows
        """
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Ponts'Chess - Play Window"))
        self.menuWindow.setTitle(_translate("MainWindow", "Window"))
        self.menuGame.setTitle(_translate("MainWindow", "Game"))
        self.menuFile.setTitle(_translate("MainWindow", "Files"))
        self.menuAI.setTitle(_translate("MainWindow", "AI"))
        self.FWP.setText(_translate("MainWindow", " Taken White Pieces "))
        self.BPP.setText(_translate("MainWindow", self.textB + " side"))
        self.FBP.setText(_translate("MainWindow", " Taken Black Pieces "))
        self.WPP.setText(_translate("MainWindow", self.textW + " side"))
        self.PontsChess.setText(_translate("MainWindow", "Ponts'Chess"))

    def DisableAllButtons(self):
        """
        Method used to disable all the playing buttons in order to show that
        the game has ended or is suspended
        """
        for PersButtLine in self.Tab:
            for PersButt in PersButtLine:
                PersButt.button.setEnabled(False)
        self.Redo.setEnabled(False)
        self.Undo.setEnabled(False)

    def EnableAllButtons(self):
        """
        Recativate all the buttons disabled by Ui_PlayWindow.DisableAllButtons
        """
        for PersButtLine in self.Tab:
            for PersButt in PersButtLine:
                PersButt.button.setEnabled(True)
        self.Redo.setEnabled(True)
        self.Undo.setEnabled(True)

    def openRules(self):
        """
        Method used to open the rules. Usually connected to the Rules menu
        """
        self.DisableAllButtons()
        self.widgetValidation.hide()
        self.widgetRules.show()

    def closeRules(self):
        """
        Closes the rules widget opened by Ui_PlayWindow.openRules
        """
        self.EnableAllButtons()
        self.widgetRules.hide()
        self.widgetValidation.show()

    def levelIA(self):
        """
        Allows to manage IA level through a window
        """
        MainWindow = QtWidgets.QMainWindow()
        self.IaLevel = AiL.Ui_LevelWindow(MainWindow, self)
        self.IaLevel.MainWindow.show()

    def handle_File(self):
        """
        Method allowing to manage the window that allows to manage the
        saved games. Usually linked to the File Menu
        """
        MainWindow = QtWidgets.QMainWindow()
        self.WindowHandle = HdF.Ui_MainWindow(
            MainWindow, self.PVP, playWindowAssoc=None
        )
        self.WindowHandle.WindowHandle.show()

    def getTakenPieces(self, FEN):
        """
        Method used when an initialisation by FEN is done
        Inputs :
            self,
            FEN, str, FEN Format. See help of __init__ method to learn more
        Goal :
            Allows to compute and add the corresponding list all the pieces
            taken in the FEN

        """
        FEN = FEN.split(" ")[0]
        self.listCount = []
        for key in numberOfPiecesFEN.keys():
            self.listCount += [numberOfPiecesFEN[key] - FEN.count(key)]
            if key == "p":
                for k in range(len(self.listCount) - 1):
                    if k % 2 == 0 and self.listCount[k] < 0:
                        self.listCount[-1] += self.listCount[k]
            elif key == "P":
                for k in range(len(self.listCount) - 1):
                    if k % 2 == 1 and self.listCount[k] < 0:
                        self.listCount[-1] += self.listCount[k]
            for piece in range(0, self.listCount[-1]):
                piece, couleur = FEN_to_Piece[key]
                nameAddedPiece = (
                    PiecesNames[piece] + ("N" if couleur == 1 else "B") + ".PNG"
                )
                iconAddedPiece = QtGui.QIcon()
                iconAddedPiece.addPixmap(
                    QtGui.QPixmap(nameAddedPiece), QtGui.QIcon.Normal, QtGui.QIcon.Off
                )
                item = QtWidgets.QListWidgetItem()
                item.setText(RealPiecesNames[piece])
                font = QtGui.QFont()
                font.setFamily("Rockwell")
                font.setPointSize(12)
                font.setBold(True)
                font.setWeight(75)
                item.setFont(font)
                item.setForeground(QtGui.QColor(255, 255, 255))
                item.setIcon(iconAddedPiece)
                if couleur == 1:
                    self.listWidget_2.addItem(item)
                else:
                    self.listWidget.addItem(item)

    def InitialisationPVP(self):
        """
        Method used in Ui_PlayWindow.Initialisation. Initialises a Player vs
        Player ChessBoard
        """

        self.DamierIA = p11m.Damier(
            "rp4PR/np4PN/bp4PB/qp4PQ/kp4PK/bp4PB/np4PN/rp4PR w KQkq - 0 1"
        )

        # ---------------------------#
        #   Creating Black Pieces   #
        # ---------------------------#

        for k in range(len(InitBlack)):
            icon = QtGui.QIcon()
            icon.addPixmap(
                QtGui.QPixmap(InitBlack[k]), QtGui.QIcon.Normal, QtGui.QIcon.Off
            )
            self.Tab[k, 0].button.setIcon(icon)
            self.Tab[k, 0].pieceAssoc = Piece(
                self.Damier, InitAssocPieces[k], 1, np.array([k, 0]), self.Tab, self.PVP
            )
            self.Damier.Dam[k + 2, 0 + 2] = 1

        iconP1 = QtGui.QIcon()
        iconP1.addPixmap(
            QtGui.QPixmap("Images_IG/Pawn_NN.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        iconP2 = QtGui.QIcon()
        iconP2.addPixmap(
            QtGui.QPixmap("Images_IG/Pawn_NB.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )

        for i in range(8):  # i correspond au numéro donc à l'abscisse et 1 à B
            self.Tab[i, 1].button.setIcon(iconP1 if i % 2 == 0 else iconP2)
            self.Tab[i, 1].pieceAssoc = Piece(
                self.Damier, 5, 1, np.array([i, 1]), self.Tab, self.PVP
            )
            self.Damier.Dam[i + 2, 1 + 2] = 1

        # ---------------------------#
        #   Creating White Pieces   #
        # ---------------------------#

        for k in range(len(InitWhite)):
            icon = QtGui.QIcon()
            icon.addPixmap(
                QtGui.QPixmap(InitWhite[k]), QtGui.QIcon.Normal, QtGui.QIcon.Off
            )
            self.Tab[k, 7].button.setIcon(icon)
            self.Tab[k, 7].pieceAssoc = Piece(
                self.Damier, InitAssocPieces[k], 2, np.array([k, 7]), self.Tab, self.PVP
            )
            self.Damier.Dam[k + 2, 7 + 2] = 2

        iconP1 = QtGui.QIcon()
        iconP1.addPixmap(
            QtGui.QPixmap("Images_IG/Pawn_BB.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        iconP2 = QtGui.QIcon()
        iconP2.addPixmap(
            QtGui.QPixmap("Images_IG/Pawn_BN.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        for i in range(8):  # i correspond au numéro donc à l'abscisse et 6 à H
            self.Tab[i, 6].button.setIcon(iconP1 if i % 2 == 0 else iconP2)
            self.Tab[i, 6].pieceAssoc = Piece(
                self.Damier, 6, 2, np.array([i, 6]), self.Tab, self.PVP
            )
            self.Damier.Dam[i + 2, 6 + 2] = 2

    def InitialisationAI(self):
        """
        Method used in Ui_PlayWindow.Initialisation. Initialises a AI vs
        Player ChessBoard
        """

        # ---------------------------#
        #   Creating Upper Pieces   #
        # ---------------------------#

        colorUpper = 1 if self.colorIA == 1 else 2
        OrderPieces = PiecesOrderBlackUp[:] if colorUpper == 1 else PiecesOrderWhiteUp
        for k in range(8):
            nameIcon = PiecesNames[OrderPieces[k]]
            nameIcon += "N" if colorUpper == 1 else "B"
            nameIcon += "N" if k % 2 == 1 else "B"
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(nameIcon), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.Tab[0, k].button.setIcon(icon)
            self.Tab[0, k].pieceAssoc = Piece(
                self.Damier,
                OrderPieces[k],
                colorUpper,
                np.array([0, k]),
                self.Tab,
                self.PVP,
            )
            self.Damier.Dam[0 + 2, k + 2] = colorUpper

        iconP1 = QtGui.QIcon()
        iconP1.addPixmap(
            QtGui.QPixmap(
                "Images_IG/Pawn_{}N.PNG".format("N" if colorUpper == 1 else "B")
            ),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        iconP2 = QtGui.QIcon()
        iconP2.addPixmap(
            QtGui.QPixmap(
                "Images_IG/Pawn_{}B.PNG".format("N" if colorUpper == 1 else "B")
            ),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )

        for j in range(8):  # i correspond au numéro donc à l'abscisse et 1 à B
            self.Tab[1, j].button.setIcon(iconP1 if j % 2 == 0 else iconP2)
            self.Tab[1, j].pieceAssoc = Piece(
                self.Damier, PawnL, colorUpper, np.array([1, j]), self.Tab, self.PVP
            )
            self.Damier.Dam[1 + 2, j + 2] = colorUpper

        # ---------------------------#
        #  Creating Player Pieces   #
        # ---------------------------#
        colorDown = 2 if self.colorIA == 1 else 1
        for k in range(8):
            nameIcon = PiecesNames[OrderPieces[k]]
            nameIcon += "N" if colorDown == 1 else "B"
            nameIcon += "N" if k % 2 == 0 else "B"
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(nameIcon), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.Tab[7, k].button.setIcon(icon)
            self.Tab[7, k].pieceAssoc = Piece(
                self.Damier,
                OrderPieces[k],
                colorDown,
                np.array([7, k]),
                self.Tab,
                self.PVP,
            )
            self.Damier.Dam[7 + 2, k + 2] = colorDown

        iconP1 = QtGui.QIcon()
        iconP1.addPixmap(
            QtGui.QPixmap(
                "Images_IG/Pawn_{}B.PNG".format("N" if colorDown == 1 else "B")
            ),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        iconP2 = QtGui.QIcon()
        iconP2.addPixmap(
            QtGui.QPixmap(
                "Images_IG/Pawn_{}N.PNG".format("N" if colorDown == 1 else "B")
            ),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        for i in range(8):  # i correspond au numéro donc à l'abscisse et 6 à H
            self.Tab[6, i].button.setIcon(iconP1 if i % 2 == 0 else iconP2)
            self.Tab[6, i].pieceAssoc = Piece(
                self.Damier, PawnR, colorDown, np.array([6, i]), self.Tab, self.PVP
            )
            self.Damier.Dam[6 + 2, i + 2] = colorDown

        if self.colorIA == 2:
            self.player_Save = 1
            self.ValidateAction()

    def InitialisationPerFEN(self, stringFEN, colorIA):
        """
        Method used in Ui_PlayWindow.Initialisation.
        Inputs :
            self,
            stringFEN, str, FEN format.
            colorIA : int. If PVP mode, please put 1 else the color played by AI
            according to the rules explaine in Ui_PlayWindow.__ini__
        Goal :
            Initialises the ChessBoard contained in the FEN
        """

        # ----------------| Removing Existing Taken pieces |----------------#
        self.listWidget.clear()
        self.listWidget_2.clear()
        self.VideLabel1.setText("-")

        # ----------------| Making sure buttons are on |----------------#
        self.Validate.clicked.disconnect()
        self.EnableAllButtons()
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap("Images_IG/bouton_valider.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.Validate.setIcon(icon)
        self.Validate.clicked.connect(self.ValidateAction)
        self.Validate.setStyleSheet("background-color : rgb(255,255,222)")

        # ----------------| Getting necessary args |----------------#
        self.DamierIA = p11m.Damier(stringFEN)
        TabFen, player, castles, halfMoves, moves = self.DecodeFEN(stringFEN, colorIA)
        self.getTakenPieces(stringFEN)

        for i in range(8):
            for j in range(8):

                # ----------------| Removing Existing Square |----------------#
                self.Tab[i, j].button.setStyleSheet(
                    self.Tab[i, j].buttonBorderDisappear
                )
                if (i + j) % 2 == 0:
                    self.Tab[i, j].button.setIcon(self.icon1)
                else:
                    self.Tab[i, j].button.setIcon(self.icon2)

                # --------------------| Adding new pieces |--------------------#
                piece, coul = TabFen[i, j][0], TabFen[i, j][1]

                if piece != None:
                    name = (
                        PiecesNames[piece]
                        + ("N" if coul == 1 else "B")
                        + ("B" if (i + j) % 2 == 0 else "N")
                    )
                    icon = QtGui.QIcon()
                    icon.addPixmap(
                        QtGui.QPixmap(name), QtGui.QIcon.Normal, QtGui.QIcon.Off
                    )
                    self.Tab[i, j].button.setIcon(icon)
                else:
                    self.Tab[i, j].button.setIcon(
                        self.icon1 if (i + j) % 2 == 0 else self.icon2
                    )

                self.Tab[i, j].pieceAssoc = (
                    Piece(
                        self.Damier, piece, coul, np.array([i, j]), self.Tab, self.PVP
                    )
                    if piece != None
                    else None
                )
                self.Damier.Dam[i + 2, j + 2] = coul
        self.player = player
        self.numberOfHalfMove = halfMoves
        self.numberOfMove = moves
        self.Damier.CastleWSmall = castles[0]
        self.Damier.CastleWGrand = castles[1]
        self.Damier.CastleBSmall = castles[2]
        self.Damier.CastleBGrand = castles[3]
        self.colorIA = colorIA
        self.retranslateUi(self.MainWindow)
        if self.player == self.colorIA:
            self.player_Save = 1
            self.ValidateAction()
        else:
            self.deplacement = False
            self.selection = True
            self.ListPossibleCase = ([], [])

    def Initialisation(self, FEN=None):
        """
        Method that initialises the chessboard
        If FEN == None, initialises AI or PVP basic chessboard else the FEN
        Chessboard.
        Attention :
            Please never use that method. It is included in the setupUI method.
            Use the aforementionned method instead.
        """
        if self.FEN == None:
            self.InitialisationPVP() if self.PVP else self.InitialisationAI()

        else:
            self.InitialisationPerFEN(FEN)

    def UndoAction(self):
        """
        Method implementing the Undo button
        """
        if self.player_Save != -1:  # Allows to know wether there has been an action
            self.DamierIA.undo_move()
            for mov in self.Mov:
                if mov != []:
                    loc = mov[0]
                    formerLoc = mov[1]
                    pieceTaken = mov[2]
                    pld.CancelMov(self.Tab, self.Damier, loc, formerLoc, pieceTaken)
                    pos_ini = 8 * formerLoc[0] + formerLoc[1]
                    pos_fin = 8 * loc[0] + loc[1]
                    if pieceTaken != None:
                        self.Tab[0, 0].RemoveTakenPiece(self.player_Save)

        if self.player_Save == 1 and self.Damier.CastleBGrand_Save != None:
            self.Damier.CastleBGrand = self.Damier.CastleBGrand_Save
            self.Damier.CastleBSmall = self.Damier.CastleBSmall_Save
            self.Damier.CastleBGrand_Save = None
            self.Damier.CastleBSmall_Save = None

        if self.player_Save == 2 and self.Damier.CastleWGrand_Save != None:
            self.Damier.CastleWGrand = self.Damier.CastleWGrand_Save
            self.Damier.CastleWSmall = self.Damier.CastleWSmall_Save
            self.Damier.CastleWGrand_Save = None
            self.Damier.CastleWSmall_Save = None

        self.player = self.player_Save  # Allowing to replay
        self.player_Save = -1  # No action played
        self.numberOfHalfMove = self.numberOfHalfMoveSave
        self.numberOfMove = self.numberOfMove - (self.player == 2)
        self.RedoPossible = True
        self.RedoList = self.Mov
        return None

    def ValidateAction(self):
        """
        Method implementing the Validation action. Allows to say that the
        turn is finished. When in AI mode, triggers automatically the move of
        the AI.
        """

        if self.player_Save != -1:  # Allows to know wether there has been an action
            self.VideLabel1.setText("-")

            # -----------------| Ending effects of the promotion |--------------------#
            if self.PromotionInProgress:
                self.PromotionInProgress = False
                self.Undo.setEnabled(True)
                self.Redo.setEnabled(True)
                self.Validate.setEnabled(True)

            # ------------------| Ending the change of castles |----------------------#
            if self.player_Save == 1:
                self.Damier.CastleBGrand_Save = None
                self.Damier.CastleBSmall_Save = None

            if self.player_Save == 2:
                self.Damier.CastleWGrand_Save = None
                self.Damier.CastleWSmall_Save = None

            # ------------------| Changing the player |------------------#
            self.player = 1 if self.player_Save == 2 else 2  # next player
            self.player_Save = -1  # No action played by the new current player

            # ------------------| Assessing the situation |------------------#
            check_ = pld.check(self.Tab, self.player)
            checkMate_ = pld.checkMate(self, self.player)
            pat_ = pld.Pat(self, self.player)
            nullGame_ = self.Damier.NullGame()

            if checkMate_:
                loser = "black" if self.player == 1 else "white"
                winner = "black" if self.player == 2 else "white"
                self.VideLabel1.setText(
                    "Check Mate for {} player, {} player wins !".format(loser, winner)
                )
                self.player = -2  # end of the game
                self.DisableAllButtons()
                self.saveGame.setEnabled(False)

                # ---------------| Exit Button |---------------#

                icon = QtGui.QIcon()
                icon.addPixmap(
                    QtGui.QPixmap("Images_IG/CloseIcon.png"),
                    QtGui.QIcon.Normal,
                    QtGui.QIcon.Off,
                )
                self.Validate.setIcon(icon)
                self.Validate.clicked.connect(self.CloseAction)
                self.Validate.setStyleSheet("background-color : rgb(185,0,0)")

            elif pat_:
                player_in_pat = "black" if self.player == 1 else "white"
                self.VideLabel1.setText(
                    "Pat for {} player, no one wins".format(player_in_pat)
                )
                self.player = -2  # end of the game
                self.DisableAllButtons()
                self.saveGame.setEnabled(False)

                # ---------------| Exit Button |---------------#

                icon = QtGui.QIcon()
                icon.addPixmap(
                    QtGui.QPixmap("Images_IG/CloseIcon.png"),
                    QtGui.QIcon.Normal,
                    QtGui.QIcon.Off,
                )
                self.Validate.setIcon(icon)
                self.Validate.clicked.connect(self.CloseAction)
                self.Validate.setStyleSheet("background-color : rgb(185,0,0)")

            elif nullGame_:
                self.VideLabel1.setText("Null Game, no one wins")
                self.player = -2  # end of the game
                self.DisableAllButtons()
                self.saveGame.setEnabled(False)

                # ---------------| Exit Button |---------------#

                icon = QtGui.QIcon()
                icon.addPixmap(
                    QtGui.QPixmap("Images_IG/CloseIcon.png"),
                    QtGui.QIcon.Normal,
                    QtGui.QIcon.Off,
                )
                self.Validate.setIcon(icon)
                self.Validate.clicked.connect(self.CloseAction)
                self.Validate.setStyleSheet("background-color : rgb(185,0,0)")

            # ---------------| AI management |---------------#

            else:
                if check_:
                    self.VideLabel1.setText(
                        "Check for {} player".format(
                            "black" if self.player == 1 else "white"
                        )
                    )

                if not self.PVP and self.colorIA == self.player:

                    # -------------| Menu Block |-------------#
                    self.saveGame.setEnabled(False)
                    self.openGame.setEnabled(False)
                    self.manageAI.setEnabled(False)

                    # ---------------| AI move |---------------#
                    pos_ini = p11m.VectorInt([-42])
                    pos_fin = p11m.VectorInt([-42])
                    prom = p11m.VectorInt([-42])
                    p11m.alpha_beta_exploration(
                        self.DamierIA, pos_ini, pos_fin, prom, self.difficultyAI
                    )

                    # ---------------| Graphic params |---------------#
                    if self.colorIA == 2:
                        pos_ini_Player = Conv_Square_IA_to_IG[pos_ini[0]]
                        pos_fin_Player = Conv_Square_IA_to_IG[pos_fin[0]]

                    else:
                        pos_ini_Player = pos_ini[0]
                        pos_fin_Player = pos_fin[0]

                    formerLoc = np.array([pos_ini_Player // 8, pos_ini_Player % 8])
                    newLoc = np.array([pos_fin_Player // 8, pos_fin_Player % 8])
                    self.Tab[formerLoc[0], formerLoc[1]].button.setStyleSheet(
                        self.Tab[0, 0].buttonBorderAppearIAMov
                    )
                    self.Tab[newLoc[0], newLoc[1]].button.setStyleSheet(
                        self.Tab[0, 0].buttonBorderAppearIAMov
                    )
                    self.MovIA = [formerLoc, newLoc]
                    self.caseSelec = formerLoc
                    castle = (
                        self.Tab[formerLoc[0], formerLoc[1]].pieceAssoc.piece == King
                        and np.max(np.abs(formerLoc - newLoc)) == 2
                    )

                    # ---------------| AI Update |---------------#
                    self.DamierIA.bouge_piece(pos_ini[0], pos_fin[0], prom[0])

                    # -------------| Menu Deblock |-------------#
                    self.saveGame.setEnabled(True)
                    self.openGame.setEnabled(True)
                    self.manageAI.setEnabled(True)

                    # ---------------| Graphic update |---------------#
                    if not castle:
                        self.Tab[newLoc[0], newLoc[1]].DeplacementNotCastle()
                        if prom[0] >= 0:
                            iconProm = QtGui.QIcon()
                            nameProm = (
                                PiecesNames[C_to_Py[prom[0]]]
                                + ("N" if self.colorIA == 1 else "B")
                                + ("B" if np.sum(newLoc) % 2 == 0 else "N")
                                + ".png"
                            )
                            iconProm.addPixmap(
                                QtGui.QPixmap(nameProm),
                                QtGui.QIcon.Normal,
                                QtGui.QIcon.Off,
                            )
                            self.Tab[newLoc[0], newLoc[1]].button.setIcon(iconProm)
                            self.Tab[newLoc[0], newLoc[1]].pieceAssoc = Piece(
                                self.Damier,
                                C_to_Py[prom[0]],
                                self.Tab[newLoc[0], newLoc[1]].pieceAssoc.couleur,
                                newLoc,
                                self.Tab,
                                self.PVP,
                            )
                        self.ValidateAction()
                    else:
                        self.Tab[newLoc[0], newLoc[1]].DeplacementForCastle()
                        self.ValidateAction()

        return None

    def RedoAction(self):
        """
        Method that implement the ReDo button
        """
        if self.RedoPossible:
            for LineButt in self.Tab:
                for Butt in LineButt:
                    Butt.button.setStyleSheet(self.Tab[0, 0].buttonBorderDisappear)
            mov_For_IA = self.RedoList[0]
            formerLoc = mov_For_IA[0]
            loc = mov_For_IA[1]
            pos_ini = 8 * formerLoc[0] + formerLoc[1]
            pos_fin = 8 * loc[0] + loc[1]
            if self.colorIA == 2:
                pos_ini = Conv_Square_IG_to_IA[pos_ini]
                pos_fin = Conv_Square_IG_to_IA[pos_fin]
            self.DamierIA.bouge_piece(pos_fin, pos_ini, -1)
            for mov in self.RedoList:
                if mov != []:
                    formerLoc = mov[0]
                    loc = mov[1]
                    pieceTaken = None
                    pld.CancelMov(self.Tab, self.Damier, loc, formerLoc, pieceTaken)
                    self.Tab[0, 0].AddTakenPiece(mov[2])

            if pieceTaken == None:
                self.numberOfHalfMove += 1
            else:
                self.numberOfHalfMove = 0  # Not necessary to save the value since it is only possible to redo after undoing and that implies that it has been saved already

            if len(self.RedoList) == 2:  # ie it is a castle
                if self.player == 1:
                    self.Damier.CastleBGrand_Save = self.Damier.CastleBGrand
                    self.Damier.CastleBSmall_Save = self.Damier.CastleBSmall
                    self.Damier.CastleBGrand = False
                    self.Damier.CastleBSmall = False

                if self.player == 2:
                    self.Damier.CastleWGrand_Save = self.Damier.CastleWGrand
                    self.Damier.CastleWSmall_Save = self.Damier.CastleWSmall
                    self.Damier.CastleWGrand = False
                    self.Damier.CastleWSmall = False

            self.numberOfMove += self.player == 2
            self.player_Save = self.player  # Current player save
            self.player = -1  # No one can play befoe validating
            self.RedoPossible = False
            self.RedoList = []
        return None

    def CloseAction(self):
        """
        Method that closes the current window and open the associated field
        self.IW. See __init__ method
        """
        self.MainWindow.close()
        self.IW.MainWindow.show()

    def EncodeFEN(self):
        """
        Method that transcript the current chessboard in a FEN format.
        Use the one implemented in moduleAI. Make small cha,ges if self.PVP
        since moduleAI is not meant to work for such situations
        """
        chaineIA = self.DamierIA.generate_FEN()
        if self.PVP:
            chaineIASplit = chaineIA.split(" ")
            chaineFEN = ""
            realCastles = ""
            # ChessBoard having undergone a rotation, IA does not calculate Castles
            # However it is still really useful to use it since it properly generates
            # FEN code. Just have to change Legit Castles Fields
            noCastle = True
            if self.Damier.CastleWSmall:
                realCastles += "K"
                noCastle = True
            if self.Damier.CastleWGrand:
                realCastles += "Q"
                noCastle = True
            if self.Damier.CastleBSmall:
                realCastles += "k"
                noCastle = True
            if self.Damier.CastleBGrand:
                realCastles += "q"
                noCastle = True
            chaineIASplit[2] = realCastles
            for k in range(6):
                chaineFEN += chaineIASplit[k]
                chaineFEN += " " if k < 5 else ""
            return chaineFEN

        else:
            return chaineIA

    def DecodeFEN(self, stringFEN, colorIA):
        """
        Method that decode a FEN
        Inputs :
            stringFEN, str, FEN format. The FEN to decipher
            colorIA, int \in {1,2} representing the color the AI is meant to
            play. If PVP mode, please enter 1
        """

        # ---------------| Docoding of AI FEN |---------------#
        ListOfFenFields = stringFEN.split(" ")
        piecesStr = ListOfFenFields[0]
        player = ListOfFenFields[1]
        castles = ListOfFenFields[2]
        halfMoves = ListOfFenFields[4]
        moves = ListOfFenFields[5]
        TabFen = np.zeros((8, 8), dtype=tuple)
        i, j = 0, 0
        castlesReal = ["K" in castles, "Q" in castles, "k" in castles, "q" in castles]
        for letter in piecesStr:
            if letter == "/":
                i += 1
                j = 0
            elif letter in "12345678":
                num = int(letter)
                for k in range(j, j + num):
                    TabFen[i, k] = (None, 0)
                j = j + num
            else:
                TabFen[i, j] = FEN_to_Piece[letter]
                if letter == "p" or letter == "P":
                    TabFen[i, j] = FEN_to_Pawn[(letter, colorIA)]
                j = j + 1
        player = 2 if player == "w" else 1
        halfMoves = int(halfMoves)
        moves = int(moves)

        # ---------------| Inversing for GI |---------------#
        if colorIA == 2:
            TabFenPlayer = np.zeros((8, 8), dtype=tuple)
            for i in range(8):
                for j in range(8):
                    pos_IA = 8 * i + j
                    pos_IG = Conv_Square_IA_to_IG[pos_IA]
                    TabFenPlayer[pos_IG // 8, pos_IG % 8] = TabFen[
                        pos_IA // 8, pos_IA % 8
                    ]
            TabFen = TabFenPlayer

        return (TabFen, player, castlesReal, halfMoves, moves)

    def SaveAction(self):
        """
        Method that allows to save the current chessboard in FEN format.
        """
        FEN = self.EncodeFEN()
        MainWindow = QtWidgets.QMainWindow()
        self.SaveWindow = ErW.Ui_SaveWindow(
            MainWindow, self.PVP, playWindowAssoc=self, FEN=FEN
        )
        self.SaveWindow.WindowSave.show()

    def OpenAction(self):
        """
        Method that allows to open a FEN format interactively.
        """
        MainWindow = QtWidgets.QMainWindow()
        self.SaveWindow = ErW.Ui_SaveWindow(MainWindow, self.PVP, playWindowAssoc=self)
        self.SaveWindow.WindowSave.show()


class Game(QtWidgets.QMainWindow):
    resized = QtCore.pyqtSignal()

    def __init__(self, PVP, IW, nameP1, nameP2=None, colorAI=None, FEN=None):
        super(Game, self).__init__(parent=None)
        self.playWin = Ui_PlayWindow(self, PVP, IW, nameP1, nameP2, colorAI, FEN)
        self.playWin.setupUi()
        self.resized.connect(self.someFunction)

    def resizeEvent(self, event):
        self.playWin.Echiquier.resizeEvent(event)
        self.resized.emit()
        return super(Game, self).resizeEvent(event)

    def someFunction(self):
        return None


if __name__ == "__main__":
    import sys
    from Initial_Window import Ui_MainWindow

    app = QtWidgets.QApplication(sys.argv)
    Iw = Ui_MainWindow()
    Iw.setupUi(QtWidgets.QMainWindow())

    g = Game(True, Iw, "Balafre", nameP2 = "GA" ,colorAI=1)
    g.show()
    sys.exit(app.exec_())
