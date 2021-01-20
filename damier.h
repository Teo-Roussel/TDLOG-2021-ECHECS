#ifndef DAMIER_H
#define DAMIER_H
#pragma once

#include "piece.h"
#include <stack>
#include <algorithm>

const int width = 8; // i indexes
const int length = 8; // j indexes


class Damier{
    Piece p_array[width*length];
    // this 1D-array represents the 2D-chessboard simply by considering
    // that lines are aggregated from the top to the bottom to create a 1D-vecor

    bool player_who_play_is_white = true; // initially, the player who start is white
    int half_move = 0; // the usual initial values
    int full_move = 1;

    bool castle_array[4] = {true, true, true, true}; // All the castles are allowed
//    0 -> left black
//    1 -> right black
//    2 -> left white
//    3 -> right white

    // all the stacks are used to store the information of the current situation
    // in order to reuse them if the method 'undo_move' is called
    std::stack<int> s_pos_ini;
    std::stack<int> s_pos_fin;
    std::stack<Piece> s_piece_moved;
    std::stack<Piece> s_piece_erased;
    std::stack<int> s_nbr_elem_back; //should be 2 if castle, 1 otherwise
    std::stack<int> s_half_move;

    std::stack<bool> s_castle_lb;
    std::stack<bool> s_castle_rb;
    std::stack<bool> s_castle_lw;
    std::stack<bool> s_castle_rw;

    /**
     * @brief add_move_to_stack : store the move from position 'pos_ini' to position 'pos_fin'.
     * Notice that there is no need to store the promotion information, since when a move will be undone,
     * the promoted piece will be again a pawn.
     * @param pos_ini (int) : the initial position of a piece
     * 0 <= pos_ini <= 63
     * @param pos_fin (int) : the final position of a piece
     * 0 <= pos_fin <= 63
     * @param nbr_moves (int) : the number of moves that have been added at this moment in the stacks above in one turn.
     * Notice that it should be at the end of a turn 2 if there is a castle (king AND rook moves)
     * And 1 if it's a normal move.
     * @throw a char* if the constraints are not verified.
     */
    void add_move_to_stack(const int pos_ini, const int pos_fin, int& nbr_moves);

public:
    /**
     * @brief Damier : construct a classical chessboard, with the black at the top
     * The white queen is on the white square
     */
    Damier();

    /**
     * @brief Damier : constructor of Damier
     * @param damier_fen (string) : a standard FEN (FEN is a standard form which represents a chessboard).
     * En-passant moves are not considered, so the corresponding composant has to be '-'
     * @throw a char* if the string is not an FEN
     */
    Damier(const std::string& damier_fen);

    /**
     * @brief operator () : allow to access to the piece at position 'pos'
     * @param pos (int) : the index of the square of the chessboard of which we want informations.
     * 0 <= pos <= 63
     * @return : a Piece object, which is at the position 'pos'
     * @throw  out_of_range if 'pos' doesn't verify the constraints
     */
    Piece operator()(const int pos) const;

    /**
     * @brief display the chessboard in the console.
     */
    void display() const;

    /**
     * @brief setPieceOnSquare : set the piece 'p' at position 'pos' on the chessboard
     * @param pos (int) : the index of the square of the chessboard on which we want to set a piece.
     * 0 <= pos <= 63
     * @param p (Piece) : the piece that is set at the square at index 'pos'
     * @throw out_of_range if 'pos' doesn't verify the constraints
     */
    void setPieceOnSquare(const int pos, const Piece p);

//    bool isCastle(const std::string& side, const bool is_player_white) const;
//    void forbidCastle(const std::string& side, const bool is_player_white);
//    void allowCastle(const std::string& side, const bool is_player_white);

    /**
     * @brief isCastle : answer to the question 'do the player of color is_player_white
     * can do the castle on the side is_side_left ?'
     * @param is_side_left (boolean) : if true, we look for the left castle.
     * If false, we look for the right castle.
     * @param is_player_white (boolean) : if true, we look for the white player
     * If false, we look for the black player.
     * @return (boolean) : true if the player can do the castle
     */
    bool isCastle(const bool is_side_left, const bool is_player_white) const;

    /**
     * @brief forbidCastle : forbid the castle on the side is_side_left
     * for the player of color is_player_white
     * @param is_side_left (boolean) : if true, we look for the left castle.
     * If false, we look for the right castle.
     * @param is_player_white (boolean) : if true, we look for the white player
     * If false, we look for the black player.
     */
    void forbidCastle(const bool is_side_left, const bool is_player_white);

    /**
     * @brief allowCastle : allow the castle on the side is_side_left
     * for the player of color is_player_white. This method is designed to be
     * only used when a move is undone.
     * @param is_side_left (boolean) : if true, we look for the left castle.
     * If false, we look for the right castle.
     * @param is_player_white (boolean) : if true, we look for the white player
     * If false, we look for the black player.
     */
    void allowCastle(const bool is_side_left, const bool is_player_white);

    /**
     * @brief getPlayerTurn : allow to know which side is currently playing.
     * @return (boolean) : if true, it's the turn of the white player
     * If false, it's the turn of the black player.
     */
    bool getPlayerTurn() const;

    /**
     * @brief getNbrFullMove : allow to know the number of full move of the game.
     * Full move is initialized to 1. It's a convention.
     * @return (int) : the number of full move of the game.
     */
    int getNbrFullMove() const;

    //bool isPieceEmpty(const int& i, const int& j) const;
    /**
     * @brief isPieceEmpty : allow to know if there is an non empty piece
     * at the position 'pos' on the chessboard.
     * @param pos (int) : 0 <= pos <= 63
     * @return (boolean) : true if the piece at position pos is a Piece("vide")/Piece(6) object.
     * False otherwise.
     * @throw out_of_range if 'pos' doesn't verify the constraints
     */
    bool isPieceEmpty(const int pos) const;


    // ===================   
    /**
     * @brief is_attacked : allow to know if one positions among those in 'positions'
     * are attacked by the opponent i.e. does an opponent piece can go in one move
     * to one of the positions.
     * @param positions (int*) : a dynamic array of positions that should be checked.
     * each element n of positions should verify : 0 <= n <= 63
     * @param nbr_positions (int) : the length of positions
     * @param adv_pos_fin (std::vector<int>) : the possible movements of the opponent
     * @return (boolean) : true if one of the positions stored in 'positions'
     * is reachable in one move by the opponent.
     * false otherwise.
     * @throw out_of_range if one the element in 'positions' is not between 0 and 63.
     */
    bool is_attacked(int* positions, const int nbr_positions, const vector<int>& adv_pos_fin) const;

    /**
     * @brief is_attacked : allow to know if the opponent can go to the square 'pos'
     * in one move.
     * @param pos (int) : the square of the chessboard that we want to know if it's under attack.
     * 0 <= pos <= 63
     * @param adv_pos_fin (std::vector<int>) : the possible movements of the opponent
     * @return (boolean) : true if the square 'pos' is reachable in one move by the opponent.
     * false otherwise.
     * @throw out_of_range is 'pos' doesn't verify the constraints.
     */
    bool is_attacked(const int pos, const vector<int>& adv_pos_fin) const;

    /**
     * @brief is_king_attacked : allow to know if the king of the player 'is_player_white' is under attack
     * @param is_player_white (boolean) : if true, we look for the white player
     * If false, we look for the black player.
     * @return (boolean) : true if the king of the player 'is_player_white' is under attack.
     * false otherwise.
     */
    bool is_king_attacked(const bool is_player_white); // renvoie un booleen indiquant si le roi de la couleur du plateau est en échec ou pas


    /**
     * @brief mvt_tour : store in 3 vectors the different informations of the theoretical moves for a rook at position 'pos'.
     * Notice that it's not checked that a rook is a position 'pos' and that moves that led the king in check are also stored.
     * @param pos : the square of the chessboard where is initially the piece of which we want to know the movements.
     * @param pos_ini_vect (std::vector<int>) : should be empty initially. After the method is called,
     * it has add to the vector the initial squares of the possible movements.
     * @param pos_fin_vect (std::vector<int>) : should be empty initially. After the method is called,
     * it has add to the vector the final squares of the possible movements.
     * @param promotion_vect (std::vector<int>) : should be empty initially. After the method is called,
     * it has add to the vector the id of the promotion if the related movement is for a pawn.
     * and if he access to the last line.
     * -1 otherwise (i.e. for all the other pieces and if a pawn is not on the last line)
     * @throw out_of_range is 'pos' doesn't verify the constraints.
     */
    void mvt_tour(const int pos, vector<int>& pos_ini_vect, vector<int>& pos_fin_vect, vector<int>& promotion_vect) const;

    /**
     * @brief mvt_fou : store in 3 vectors the different informations of the theoretical moves for a bishop at position 'pos'.
     * Notice that it's not checked that a bishop is a position 'pos' and that moves that led the king in check are also stored.
     * @param pos : the square of the chessboard where is initially the piece of which we want to know the movements.
     * 0 <= pos <= 63
     * @param pos_ini_vect (std::vector<int>) : should be empty initially. After the method is called,
     * it has add to the vector the initial squares of the possible movements.
     * @param pos_fin_vect (std::vector<int>) : should be empty initially. After the method is called,
     * it has add to the vector the final squares of the possible movements.
     * @param promotion_vect (std::vector<int>) : should be empty initially. After the method is called,
     * it has add to the vector the id of the promotion if the related movement is for a pawn.
     * and if he access to the last line.
     * -1 otherwise (i.e. for all the other pieces and if a pawn is not on the last line)
     * @throw out_of_range is 'pos' doesn't verify the constraints.
     */
    void mvt_fou(const int pos, vector<int>& pos_ini_vect, vector<int>& pos_fin_vect, vector<int>& promotion_vect) const;

    /**
     * @brief mvt_cavalier : store in 3 vectors the different informations of the theoretical moves for a knight at position 'pos'.
     * Notice that it's not checked that a knight is a position 'pos' and that moves that led the king in check are also stored.
     * @param pos : the square of the chessboard where is initially the piece of which we want to know the movements.
     * 0 <= pos <= 63
     * @param pos_ini_vect (std::vector<int>) : should be empty initially. After the method is called,
     * it has add to the vector the initial squares of the possible movements.
     * @param pos_fin_vect (std::vector<int>) : should be empty initially. After the method is called,
     * it has add to the vector the final squares of the possible movements.
     * @param promotion_vect (std::vector<int>) : should be empty initially. After the method is called,
     * it has add to the vector the id of the promotion if the related movement is for a pawn.
     * and if he access to the last line.
     * -1 otherwise (i.e. for all the other pieces and if a pawn is not on the last line)
     * @throw out_of_range is 'pos' doesn't verify the constraints.
     */
    void mvt_cavalier(const int pos, vector<int>& pos_ini_vect, vector<int>& pos_fin_vect, vector<int>& promotion_vect) const;

    /**
     * @brief mvt_dame : store in 3 vectors the different informations of the theoretical moves for a queen at position 'pos'.
     * Notice that it's not checked that a queen is a position 'pos' and that moves that led the king in check are also stored.
     * @param pos : the square of the chessboard where is initially the piece of which we want to know the movements.
     * 0 <= pos <= 63
     * @param pos_ini_vect (std::vector<int>) : should be empty initially. After the method is called,
     * it has add to the vector the initial squares of the possible movements.
     * @param pos_fin_vect (std::vector<int>) : should be empty initially. After the method is called,
     * it has add to the vector the final squares of the possible movements.
     * @param promotion_vect (std::vector<int>) : should be empty initially. After the method is called,
     * it has add to the vector the id of the promotion if the related movement is for a pawn.
     * and if he access to the last line.
     * -1 otherwise (i.e. for all the other pieces and if a pawn is not on the last line)
     * @throw out_of_range is 'pos' doesn't verify the constraints.
     */
    void mvt_dame(const int pos, vector<int>& pos_ini_vect, vector<int>& pos_fin_vect, vector<int>& promotion_vect) const;

    /**
     * @brief mvt_roi : store in 3 vectors the different informations of the theoretical moves for a king at position 'pos'.
     * Notice that it's not checked that a king is a position 'pos' and that moves that led the king in check are also stored.
     * @param pos : the square of the chessboard where is initially the piece of which we want to know the movements.
     * 0 <= pos <= 63
     * @param pos_ini_vect (std::vector<int>) : should be empty initially. After the method is called,
     * it has add to the vector the initial squares of the possible movements.
     * @param pos_fin_vect (std::vector<int>) : should be empty initially. After the method is called,
     * it has add to the vector the final squares of the possible movements.
     * @param promotion_vect (std::vector<int>) : should be empty initially. After the method is called,
     * it has add to the vector the id of the promotion if the related movement is for a pawn.
     * and if he access to the last line.
     * -1 otherwise (i.e. for all the other pieces and if a pawn is not on the last line)
     * @param callIs_attacked (boolean) : if true, the castle moves (if they are possible and still allowed)
     * are added to the vector of movements.
     * @throw out_of_range is 'pos' doesn't verify the constraints.
     */
    void mvt_roi(const int pos,vector<int>& pos_ini_vect, vector<int>& pos_fin_vect, vector<int>& promotion_vect, const bool callIs_attacked) const;

    /**
     * @brief mvt_pion : store in 3 vectors the different informations of the theoretical moves for a pawn at position 'pos'.
     * Notice that it's not checked that a pawn is a position 'pos' and that moves that led the king in check are also stored.
     * @param pos : the square of the chessboard where is initially the piece of which we want to know the movements.
     * 0 <= pos <= 63
     * @param pos_ini_vect (std::vector<int>) : should be empty initially. After the method is called,
     * it has add to the vector the initial squares of the possible movements.
     * @param pos_fin_vect (std::vector<int>) : should be empty initially. After the method is called,
     * it has add to the vector the final squares of the possible movements.
     * @param promotion_vect (std::vector<int>) : should be empty initially. After the method is called,
     * it has add to the vector the id of the promotion if the related movement is for a pawn.
     * and if he access to the last line.
     * -1 otherwise (i.e. for all the other pieces and if a pawn is not on the last line)
     * @throw out_of_range is 'pos' doesn't verify the constraints.
     */
    void mvt_pion(const int pos, vector<int>& pos_ini_vect, vector<int>& pos_fin_vect, vector<int>& promotion_vect) const;

    /**
     * @brief movement_piece : store in 3 vectors the different informations of the theoretical moves for the piece on square 'pos'.
     * Notice that in this method, it checks which piece is on square 'pos'. It still stores the moves that led the king in check.
     * Notice also that there is no move for an empty piece, so the vector are not modified.
     * @param pos : the square of the chessboard where is initially the piece of which we want to know the movements.
     * 0 <= pos <= 63
     * @param pos_ini_vect (std::vector<int>) : should be empty initially. After the method is called,
     * it has add to the vector the initial squares of the possible movements.
     * @param pos_fin_vect (std::vector<int>) : should be empty initially. After the method is called,
     * it has add to the vector the final squares of the possible movements.
     * @param promotion_vect (std::vector<int>) : should be empty initially. After the method is called,
     * it has add to the vector the id of the promotion if the related movement is for a pawn.
     * and if he access to the last line.
     * -1 otherwise (i.e. for all the other pieces and if a pawn is not on the last line)
     * @param callIs_attacked (boolean) : if true, the castle moves (if they are possible and still allowed)
     * are added to the vector of movements.
     * @throw out_of_range is 'pos' doesn't verify the constraints.
     */
    void movement_piece(const int pos, vector<int>& pos_ini_vect, vector<int>& pos_fin_vect, vector<int>& promotion_vect, const bool callIs_attacked) const;

    /**
     * @brief player_possible_movements : store in 3 vectors the different informations
     * of the theoretical moves for the player of color 'is_player_white'.
     * Notice that it stores the moves that led the king in check.
     * @param is_player_white (boolean) : if true, we look for the white player
     * If false, we look for the black player.
     * @param pos_ini_vect (std::vector<int>) : should be empty initially. After the method is called,
     * it has add to the vector the initial squares of the possible movements.
     * @param pos_fin_vect (std::vector<int>) : should be empty initially. After the method is called,
     * it has add to the vector the final squares of the possible movements.
     * @param promotion_vect (std::vector<int>) : should be empty initially. After the method is called,
     * it has add to the vector the id of the promotion if the related movement is for a pawn.
     * and if he access to the last line.
     * -1 otherwise (i.e. for all the other pieces and if a pawn is not on the last line)
     * @param callIs_attacked (boolean) : if true, the castle moves (if they are possible and still allowed)
     * are added to the vector of movements.
     */
    void player_possible_movements(const bool is_player_white, vector<int>& pos_ini_vect, vector<int>& pos_fin_vect, vector<int>& promotion_vect, const bool callIs_attacked = true) const;

    /**
     * @brief bouge_piece : move the piece at position 'pos_ini' to the position 'pos_fin'.
     * If promotion is not equal to -1, the piece is promoted to the piece with id 'promotion'.
     * Notice that you can move an empty piece.
     * @param pos_ini (int) : the initial position of a piece
     * 0 <= pos_ini <= 63
     * @param pos_fin (int) : the final position of a piece
     * 0 <= pos_fin <= 63
     * @param promotion (int) : the new id of the final piece.
     * If promotion == -1, there is no promotion (the new id is the initial id of the piece)
     * -1 <= promotion <= 5
     * @effect : invert the boolean which represents the color of the player who plays, stored in this chessboard object.
     * @effect : update the value of half_move.
     * @effect : update the value of full_move.
     * @effect : update the boolean which represents the possibility to do the castle moves.
     * @effect : invert the boolean which represents the color of the player who plays, stored in this chessboard object.
     * @return (boolean) : true if it the move lets the king of color in check.
     * false otherwise.
     * @throw out_of_range is 'pos_ini' or 'pos_fin' don't verify the constraints.
     * @throw a char* if 'promotion' doesn't verify the constraints.
     */
    bool bouge_piece(const int pos_ini, const int pos_fin, const int promotion);

    /**
     * @brief undo_move : undo the last move done.
     */
    void undo_move();

    /**
     * @brief generateFEN : create a string which containt the standard format FEN,
     * which is used to represent the state of a chessboard.
     * @return (string) : a string which represents the FEN format of the current state of the chessboard.
     */
    string generateFEN();
};


/**
 * @brief push_multiple_elem : push multiple elements in multiple vectors (respectively)
 * @param v1 (int) : the value that will be push in vect1
 * @param vect1 (std::vector<int>) : the first vector
 * @param v2 (int) : the value that will be push in vect2
 * @param vect2 (std::vector<int>) : the second vector
 * @param v3 (int) : the value that will be push in vect3
 * @param vect3 (std::vector<int>) : the third vector
 */
void push_multiple_elem(const int& v1, vector<int>& vect1, const int& v2, vector<int>& vect2, const int v3, vector<int>& vect3);



#endif // DAMIER_H
