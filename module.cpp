#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>
#include <pybind11/stl_bind.h>

#include <functional>
#include <iostream>

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <map>
#include <vector>

PYBIND11_MAKE_OPAQUE(std::vector<int>);

// =======| Include of our files |===========
#include <piece.h>
#include <piece.cpp>
#include <damier.h>
#include <damier.cpp>
#include <engine.h>
#include <engine.cpp>


PYBIND11_MODULE(moduleAI, module)
{
	module.doc() = "Documentation of moduleAI";
	
	// we link the different types of vectors thanks to the pybind11 header
	// this is mandatory because we have objects passed by reference in functions.
	// if we wanted, for non-classical classes, we could recode these 'bind' ourselves
	pybind11::bind_vector<std::vector<int>>(module, "VectorInt");

	// it's a template
	pybind11::class_<Piece>(module, "Piece")
		.def(pybind11::init<>())
		.def(pybind11::init<std::string, bool>(), "second constructor", pybind11::arg("piece_name"), pybind11::arg("is_white"))
		.def("getName", &Piece::getName, "return the name of the Piece object")
		.def("isWhite", &Piece::isWhite)
		.def("getId", &Piece::getId)
	
		.def(pybind11::self == pybind11::self)
		.def(pybind11::self != pybind11::self)		
		.def_property_readonly("name", &Piece::getName)
		.def_property_readonly("Id", &Piece::getId)
		.def_property_readonly("is_white", &Piece::isWhite)

		.def("__repr__", [](const Piece& p) { return "pybind11module.Piece named " + ((p.getName() == "vide") ? "vide" : (p.isWhite() ? (p.getName() + " Blanc") : (p.getName() + " Noir"))); })
		.def("__str__", [](const Piece& p) { return ((p.getName() == "vide") ? "    v    " : (p.isWhite() ? (p.getName() + " Blanc") : (p.getName() + " Noir"))); })
	;	

	pybind11::class_<Damier>(module, "Damier")
		.def(pybind11::init<>())		
		.def(pybind11::init<std::string>(), "FEN constructor", pybind11::arg("damier_fen"))
		.def("__call__", &Damier::operator())
		.def("display", &Damier::display)
		.def("setPieceOnSquare", &Damier::setPieceOnSquare, pybind11::arg("pos"), pybind11::arg("piece"))
		.def("isCastle", &Damier::isCastle, pybind11::arg("side"), pybind11::arg("is_player_white"))
		.def("forbidCastle", &Damier::forbidCastle, pybind11::arg("side"), pybind11::arg("is_player_white"))
		.def("allowCastle", &Damier::allowCastle, pybind11::arg("side"), pybind11::arg("is_player_white"))
		.def("getPlayerTurn", &Damier::getPlayerTurn)
		.def("isPieceEmpty", &Damier::isPieceEmpty, pybind11::arg("pos"))
		
		.def("is_king_attacked", &Damier::is_king_attacked)

		.def("mvt_tour", &Damier::mvt_tour, pybind11::arg("pos"), pybind11::arg("pos_ini_vect"), pybind11::arg("pos_fin_vect"), pybind11::arg("promotion_vect"))
		.def("mvt_fou", &Damier::mvt_fou, pybind11::arg("pos"), pybind11::arg("pos_ini_vect"), pybind11::arg("pos_fin_vect"), pybind11::arg("promotion_vect"))
		.def("mvt_cavalier", &Damier::mvt_cavalier, pybind11::arg("pos"), pybind11::arg("pos_ini_vect"), pybind11::arg("pos_fin_vect"), pybind11::arg("promotion_vect"))
		.def("mvt_dame", &Damier::mvt_dame, pybind11::arg("pos"), pybind11::arg("pos_ini_vect"), pybind11::arg("pos_fin_vect"), pybind11::arg("promotion_vect"))
		.def("mvt_roi", &Damier::mvt_roi, pybind11::arg("pos"), pybind11::arg("pos_ini_vect"), pybind11::arg("pos_fin_vect"), pybind11::arg("promotion_vect"), pybind11::arg("callIs_attacked"))
		.def("mvt_pion", &Damier::mvt_pion, pybind11::arg("pos"), pybind11::arg("pos_ini_vect"), pybind11::arg("pos_fin_vect"), pybind11::arg("promotion_vect"))
		
		.def("movement_piece", &Damier::movement_piece, pybind11::arg("pos"), pybind11::arg("pos_ini_vect"), pybind11::arg("pos_fin_vect"), pybind11::arg("prom_vect"), pybind11::arg("callIs_attacked"))
		.def("player_possible_movements", &Damier::player_possible_movements, pybind11::arg("is_player_white"), pybind11::arg("pos_ini_vect"), pybind11::arg("pos_fin_vect"), pybind11::arg("prom_vect"), pybind11::arg("callIs_attacked"))
		.def("bouge_piece", &Damier::bouge_piece, pybind11::arg("pos_ini"), pybind11::arg("pos_fin"), pybind11::arg("promotion"))
		
		.def("undo_move", &Damier::undo_move)
		.def("generate_FEN", &Damier::generateFEN)
	;

	module.def("evaluate_bonus_malus", &evaluate_bonus_malus, pybind11::arg("chessboard"), pybind11::arg("is_player_white"));
	module.def("alpha_beta_exploration", &alpha_beta_exploration, pybind11::arg("chessboard"), pybind11::arg("pos_ini"), pybind11::arg("pos_fin"), pybind11::arg("promotion"), pybind11::arg("depth"));
}
