#ifndef ENGINE_H
#define ENGINE_H
#pragma once

#include "piece.h"
#include "damier.h"
#include <unordered_map>


/**
 * @brief evaluate_bonus_malus : compute the value of a chessboard, according to a specific point of view
 * @param chessboard (Damier) : the Damier object for which we want to know the evaluation
 * @param is_player_white (boolean) : if true, we want to know the evaluation from the point of view of white player
 * Otherwise, from the point of view of black player.
 * @return (int) : the value of a chessboard, according to the point of view passed with 'is_player_white'
 */
int evaluate_bonus_malus(const Damier& chessboard, const bool is_player_white);

/**
 * @brief alpha_beta_exploration : compute the best move for the AI, for a fixed depth.
 * @param chessboard (Chessboard) : the chessboard on which we want to make the AI play.
 * @param pos_ini (int) : will be the initial position of the best move
 * will verify after execution 0 <= pos_ini <= 63
 * @param pos_fin (int) : will be the final position of the best move
 * will verify after execution 0 <= pos_fin <= 63
 * @param promotion (int) : will be the id of the promotion for the best move
 * Or -1 if there is no promotion.
 * will verify after execution -1 <= promotion <= 3
 * @param depth (int) : the depth in the negamax algorithm
 */
void alpha_beta_exploration(Damier& chessboard, vector<int> &pos_ini, vector<int> &pos_fin, vector<int> &promotion, const int depth);

/**
 * @brief alpha_beta_exploration_aux : return the best value (for the best move) for the AI, at depth 'depth'
 * @param chessboard (Chessboard) : the chessboard on which we want to make the AI play.
 * @param depth (int) : the depth in the negamax algorithm
 * @param alpha (int) : the lower bound
 * @param beta (int) : the upper bound
 * @param nbr_iter (int) : the number of iterations
 * @return (int) : the better value found at the depth 'depth'
 */
int alpha_beta_exploration_aux(Damier& chessboard, const int depth, int alpha, int beta, int &nbr_iter);

#endif // ENGINE_H
