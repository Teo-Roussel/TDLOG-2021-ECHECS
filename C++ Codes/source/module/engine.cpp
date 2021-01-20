#include "engine.h"
#include "piece.h"
#include "damier.h"

#include <ctime>
using namespace std;


// =========| Bonus and malus tables for white pieces |===============

static const int white_pawn_values[64] = { 0, 0, 0, 0, 0, 0, 0, 0,
                                    50, 50, 50, 50, 50, 50, 50, 50,
                                    10, 10, 20, 30, 30, 20, 10, 10,
                                    5, 5, 10, 25, 25, 10, 5, 5,
                                    0, 0, 0, 20, 20, 0, 0, 0,
                                    5, -5, -10, 0, 0, -10, -5, 5,
                                    5, 10, 10, -20, -20, 10, 10, 5,
                                    0, 0, 0, 0, 0, 0, 0, 0
};

static const int white_knight_values[64] = { -50, -40, -30, -30, -30, -30, -40, -50,
                                      -40, -20, 0, 0, 0, 0, -20, -40,
                                      -30, 0, 10, 15, 15, 10, 0, -30,
                                      -30, 5, 15, 20, 20, 15, 5, -30,
                                      -30, 0, 15, 20, 20, 15, 0, -30,
                                      -30, 5, 10, 15, 15, 10, 5, -30,
                                      -40, -20, 0, 5, 5, 0, -20, -40,
                                      -50, -40, -30, -30, -30, -30, -40, -50
};

static const int white_bishop_values[64] = { -20, -10, -10, -10, -10, -10, -10, -20,
                                      -10, 0, 0, 0, 0, 0, 0, -10,
                                      -10, 0, 5, 10, 10, 5, 0, -10,
                                      -10, 5, 5, 10, 10, 5, 5, -10,
                                      -10, 0, 10, 10, 10, 10, 0, -10,
                                      -10, 10, 10, 10, 10, 10, 10, -10,
                                      -10, 5, 0, 0, 0, 0, 5, -10,
                                      -20, -10, -10, -10, -10, -10, -10, -20
};

static const int white_rook_values[64] = { 0, 0, 0, 0, 0, 0, 0, 0,
                                    5, 10, 10, 10, 10, 10, 10, 5,
                                    -5, 0, 0, 0, 0, 0, 0, -5,
                                    -5, 0, 0, 0, 0, 0, 0, -5,
                                    -5, 0, 0, 0, 0, 0, 0, -5,
                                    -5, 0, 0, 0, 0, 0, 0, -5,
                                    -5, 0, 0, 0, 0, 0, 0, -5,
                                    0, 0, 0, 5, 5, 0, 0, 0
};

static const int white_queen_values[64] = { -20, -10, -10, -5, -5, -10, -10, -20,
                                     -10, 0, 0, 0, 0, 0, 0, -10,
                                     -10, 0, 5, 5, 5, 5, 0, -10,
                                     -5, 0, 5, 5, 5, 5, 0, -5,
                                     0, 0, 5, 5, 5, 5, 0, -5,
                                     -10, 5, 5, 5, 5, 5, 0, -10,
                                     -10, 0, 5, 0, 0, 0, 0, -10,
                                     -20, -10, -10, -5, -5, -10, -10, -20
};

static const int white_king_values_middle_game[64] = { -30, -40, -40, -50, -50, -40, -40, -30,
                                                -30, -40, -40, -50, -50, -40, -40, -30,
                                                -30, -40, -40, -50, -50, -40, -40, -30,
                                                -30, -40, -40, -50, -50, -40, -40, -30,
                                                -20, -30, -30, -40, -40, -30, -30, -20,
                                                -10, -20, -20, -30, -30, -20, -20, -10,
                                                20, 20, 0, 0, 0, 0, 20, 20,
                                                20, 30, 10, 0, 0, 10, 30, 20
};

static const int white_king_values_end_game[64] = { -50, -40, -30, -20, -20, -30, -40, -50,
                                                -30, -20, -10, 0, 0, -10, -20, -30,
                                                -30, -10, 20, 30, 30, 20, -10, -30,
                                                -30, -10, 30, 40, 40, 30, -10, -30,
                                                -30, -10, 30, 40, 40, 30, -10, -30,
                                                -30, -10, 20, 30, 30, 20, -10, -30,
                                                -30, -30, 0, 0, 0, 0, -30, -30,
                                                -50, -30, -30, -30, -30, -30, -30, -50
};

// =========| Bonus and malus tables for black pieces |===============

static const int black_pawn_values[64] = { 0, 0, 0, 0, 0, 0, 0, 0,
                                    5, 10, 10, -20, -20, 10, 10, 5,
                                    5, -5, -10, 0, 0, -10, -5, 5,
                                    0, 0, 0, 20, 20, 0, 0, 0,
                                    5, 5, 10, 25, 25, 10, 5, 5,
                                    10, 10, 20, 30, 30, 20, 10, 10,
                                    50, 50, 50, 50, 50, 50, 50, 50,
                                    0, 0, 0, 0, 0, 0, 0, 0
};

static const int black_knight_values[64] = { -50, -40, -30, -30, -30, -30, -40, -50,
                                      -40, -20, 0, 5, 5, 0, -20, -40,
                                      -30, 5, 10, 15, 15, 10, 5, -30,
                                      -30, 0, 15, 20, 20, 15, 0, -30,
                                      -30, 5, 15, 20, 20, 15, 5, -30,
                                      -30, 0, 10, 15, 15, 10, 0, -30,
                                      -40, -20, 0, 0, 0, 0, -20, -40,
                                      -50, -40, -30, -30, -30, -30, -40, -50
};

static const int black_bishop_values[64] = { -20, -10, -10, -10, -10, -10, -10, -20,
                                      -10, 5, 0, 0, 0, 0, 5, -10,
                                      -10, 10, 10, 10, 10, 10, 10, -10,
                                      -10, 0, 10, 10, 10, 10, 0, -10,
                                      -10, 5, 5, 10, 10, 5, 5, -10,
                                      -10, 0, 5, 10, 10, 5, 0, -10
                                      - 10, 0, 0, 0, 0, 0, 0, -10,
                                      -20, -10, -10, -10, -10, -10, -10, -20
};

static const int black_rook_values[64] = { 0, 0, 0, 5, 5, 0, 0, 0,
                                    -5, 0, 0, 0, 0, 0, 0, -5,
                                    -5, 0, 0, 0, 0, 0, 0, -5,
                                    -5, 0, 0, 0, 0, 0, 0, -5,
                                    -5, 0, 0, 0, 0, 0, 0, -5,
                                    -5, 0, 0, 0, 0, 0, 0, -5,
                                    5, 10, 10, 10, 10, 10, 10, 5,
                                    0, 0, 0, 0, 0, 0, 0, 0
};


static const int black_queen_values[64] = { -20, -10, -10, -5, -5, -10, -10, -20,
                                     -10, 0, 0, 0, 0, 5, 0, -10,
                                     -10, 0, 5, 5, 5, 5, 5, -10,
                                     0, 0, 5, 5, 5, 5, 0, -5,
                                     -5, 0, 5, 5, 5, 5, 0, -5,
                                     -10, 0, 5, 5, 5, 5, 0, -10,
                                     -10, 0, 0, 0, 0, 0, 0, -10,
                                     -20, -10, -10, -5, -5, -10, -10, -20
};

static const int black_king_values_middle_game[64] = { 20, 30, 10, 0, 0, 10, 30, 20,
                                                20, 20, 0, 0, 0, 0, 20, 20,
                                                -10, -20, -20, -30, -30, -20, -20, -10,
                                                -20, -30, -30, -40, -40, -30, -30, -20,
                                                -30, -40, -40, -50, -50, -40, -40, -30,
                                                -30, -40, -40, -50, -50, -40, -40, -30,
                                                -30, -40, -40, -50, -50, -40, -40, -30,
                                                -30, -40, -40, -50, -50, -40, -40, -30
};

static const int black_king_values_end_game[64] = { -50, -30, -30, -30, -30, -30, -30, -50,
                                             -30, -30, 0, 0, 0, 0, -30, -30,
                                             -30, -10, 20, 30, 30, 20, -10, -30,
                                             -30, -10, 30, 40, 40, 30, -10, -30,
                                             -30, -10, 30, 40, 40, 30, -10, -30,
                                             -30, -10, 20, 30, 30, 20, -10, -30,
                                             -30, -20, -10, 0, 0, -10, -20, -30,
                                             -50, -40, -30, -20, -20, -30, -40, -50
};


// =================| IA Functions |=======================

int evaluate_bonus_malus(const Damier& chessboard, const bool is_player_white) {
    static const int fin_de_partie = 20;
    int white_score = 0;
    int black_score = 0;
    // ==================| Computation of each player's values |==================
    for (int pos = 0; pos < width * length; pos++)
    {
        int current_id = chessboard(pos).getId();
        if (current_id == 6)
            continue;

        if (chessboard(pos).isWhite())
        {
            white_score += mapOfValues_.at(current_id);
            if (current_id == 5)
                white_score += white_pawn_values[pos];
            else if (current_id == 1)
                white_score += white_knight_values[pos];
            else if (current_id == 2)
                white_score += white_bishop_values[pos];
            else if (current_id == 0)
                white_score += white_rook_values[pos];
            else if (current_id == 3)
                white_score += white_queen_values[pos];
            else if (current_id == 4 && chessboard.getNbrFullMove() < fin_de_partie)
                white_score += white_king_values_middle_game[pos];
            else if (current_id == 4 && chessboard.getNbrFullMove() >= fin_de_partie)
                white_score += white_king_values_end_game[pos];
            else
                throw "Error in the computation of the score";
        }
        else
        {
            black_score += mapOfValues_.at(current_id);
            if (current_id == 5)
                black_score += black_pawn_values[pos];
            else if (current_id == 1)
                black_score += black_knight_values[pos];
            else if (current_id == 2)
                black_score += black_bishop_values[pos];
            else if (current_id == 0)
                black_score += black_rook_values[pos];
            else if (current_id == 3)
                black_score += black_queen_values[pos];
            else if (current_id == 4 && chessboard.getNbrFullMove() < fin_de_partie)
                black_score += black_king_values_middle_game[pos];
            else if (current_id == 4 && chessboard.getNbrFullMove() >= fin_de_partie)
                black_score += black_king_values_end_game[pos];
            else
                throw "Error in the computation of the score";
        }
    }
    if (is_player_white)
        return white_score - black_score;
    else
        return black_score - white_score;    
}

// ===============| Negamax with alpha-beta pruning implementation |==============

void alpha_beta_exploration(Damier& chessboard, vector<int> &pos_ini, vector<int> &pos_fin, vector<int> &promotion, const int depth){
    if (depth < 1) {
        throw "depth should be superior or equal to 1";
    }    

    int alpha = -40000;
    int beta = 40000;
    int value = -60000; // equivalent to -infiny
    vector<int> pos_ini_vect;
    vector<int> pos_fin_vect;
    vector<int> promotion_vect;
    chessboard.player_possible_movements(chessboard.getPlayerTurn(), pos_ini_vect, pos_fin_vect, promotion_vect, true);
    int nbr_iter = 0;  

    for (unsigned int k = 0; k < pos_ini_vect.size(); k++){       

        if (!chessboard.bouge_piece(pos_ini_vect[k], pos_fin_vect[k], promotion_vect[k])){ 
            // if the move is invalid, we do not look at him, and continue our search
            chessboard.undo_move();
            continue;
        }

        int val_int = - alpha_beta_exploration_aux(chessboard, depth-1, -beta, -alpha, nbr_iter);
        chessboard.undo_move(); // once the move has been processed, it is undone in order to process the next moves        

        if (val_int > value){
            // Storage of the best move
            pos_ini[0] = pos_ini_vect[k];
            pos_fin[0] = pos_fin_vect[k];
            promotion[0] = promotion_vect[k];
            value = val_int;
        }
       
        if (value > alpha)
            alpha = value;
        if (value >= beta)
            break;        
    }   
}


int alpha_beta_exploration_aux(Damier& chessboard, const int depth, int alpha, int beta, int& nbr_iter){        
    if (depth == 0)       
        return evaluate_bonus_malus(chessboard, chessboard.getPlayerTurn());

    int value = -60000; // equivalent to -infiny
    vector<int> pos_ini_vect;
    vector<int> pos_fin_vect;
    vector<int> promotion_vect;
    chessboard.player_possible_movements(chessboard.getPlayerTurn(), pos_ini_vect, pos_fin_vect, promotion_vect, true);

    bool valid_move_exist = false;
    for (unsigned int k = 0; k < pos_ini_vect.size(); k++){
        
        if (!chessboard.bouge_piece(pos_ini_vect[k], pos_fin_vect[k], promotion_vect[k])){
            // if the move is invalid, we do not look at him, and continue our search
            chessboard.undo_move();
            continue;
        }
        valid_move_exist = true;

        value = max(value, -alpha_beta_exploration_aux(chessboard, depth-1, -beta, -alpha, nbr_iter));        
        chessboard.undo_move(); // once the move has been processed, it is undone in order to process the next moves    
        
        alpha = max(alpha, value);
        if (alpha >= beta)
            break;       
    }
    
    if (!valid_move_exist){
        if (chessboard.is_king_attacked(chessboard.getPlayerTurn())){  
            // -20000 is added to represent the fact that the king will always be caught
            return (-20000+evaluate_bonus_malus(chessboard, chessboard.getPlayerTurn()) )  * max(1,int(depth/2.0));
        }
        else
            return 0; // draw
    }   

    return value;
}
