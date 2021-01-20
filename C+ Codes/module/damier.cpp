#include "damier.h"
#include <string>
using namespace std;

static const int a8 = 0;
static const int b8 = 1;
static const int c8 = 2;
static const int d8 = 3;
static const int e8 = 4;
static const int f8 = 5;
static const int g8 = 6;
static const int h8 = 7;

static const int a1 = 56;
static const int b1 = 57;
static const int c1 = 58;
static const int d1 = 59;
static const int e1 = 60;
static const int f1 = 61;
static const int g1 = 62;
static const int h1 = 63;

static const int array_64 [width*length] = {21 , 22 , 23 , 24 , 25 , 26 , 27 , 28 ,
                31 , 32 , 33 , 34 , 35 , 36 , 37 , 38 ,
                41 , 42 , 43 , 44 , 45 , 46 , 47 , 48 ,
                51 , 52 , 53 , 54 , 55 , 56 , 57 , 58 ,
                61 , 62 , 63 , 64 , 65 , 66 , 67 , 68 ,
                71 , 72 , 73 , 74 , 75 , 76 , 77 , 78 ,
                81 , 82 , 83 , 84 , 85 , 86 , 87 , 88 ,
                91 , 92 , 93 , 94 , 95 , 96 , 97 , 98 };

static const int array_120[width*length + width*(length-1)] = {-1 , -1 , -1 , -1 , -1 , -1 , -1 , -1 , -1 , -1 ,
                                                      -1 , -1 , -1 , -1 , -1 , -1 , -1 , -1 , -1 , -1 ,
                                                      -1 , 0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , -1 ,
                                                      -1 , 8 , 9 , 10 , 11 , 12 , 13 , 14 , 15 , -1 ,
                                                      -1 , 16 , 17 , 18 , 19 , 20 , 21 , 22 , 23 , -1 ,
                                                      -1 , 24 , 25 , 26 , 27 , 28 , 29 , 30 , 31 , -1 ,
                                                      -1 , 32 , 33 , 34 , 35 , 36 , 37 , 38 , 39 , -1 ,
                                                      -1 , 40 , 41 , 42 , 43 , 44 , 45 , 46 , 47 , -1 ,
                                                      -1 , 48 , 49 , 50 , 51 , 52 , 53 , 54 , 55 , -1 ,
                                                      -1 , 56 , 57 , 58 , 59 , 60 , 61 , 62 , 63 , -1 ,
                                                      -1 , -1 , -1 , -1 , -1 , -1 , -1 , -1 , -1 , -1 ,
                                                      -1 , -1 , -1 , -1 , -1 , -1 , -1 , -1 , -1 , -1 };


Damier::Damier(){    

    for (int i = 0; i < width/2; i++)
    {
        // ==================| Construction of the black pieces |================
        p_array[i + width*0] = Piece(name_array[i], false);
        p_array[width - 1- i + width*0] = Piece(name_array[i], false);
        p_array[i + width*1] = Piece("pion", false);
        p_array[width - 1 - i + width*1] = Piece("pion", false);

        // ==================| Construction of the white pieces |================
        p_array[i + width*(length-1)] = Piece(name_array[i], true);
        p_array[width - 1 - i + width*(length-1)] = Piece(name_array[i], true);
        p_array[i + width*(length-2)] = Piece("pion", true);
        p_array[width - 1 - i + width*(length-2)] = Piece("pion", true);
    }
    // ====================| Management of non-symmetrical cases |===============
    p_array[width/2 + width*0] = Piece("roi", false);
    p_array[width/2 + width*(length-1)] = Piece("roi", true);
};


Damier::Damier(const string& damier_fen){
    int n = damier_fen.length();
    int nbr_slash = 0;
    int nbr_espace = 0;
    int ind_ligne = 0;

    bool color_found = false;
    bool castle_found = false;
    bool en_passant_found = false;
    bool half_move_found = false;
    bool full_move_found = false;

    for (int k = 0; k < n; k++)
    {
        if (nbr_espace == 0)
        {          
            if (damier_fen[k] == '/')
            {
                nbr_slash++;
                ind_ligne = 0;
            }
            else if (damier_fen[k] == 'r')
            {
                if (ind_ligne >= 8)
                    throw "Invalid chain";
                p_array[ind_ligne + nbr_slash*width] = Piece("tour", false);
                ind_ligne++;
            }
            else if (damier_fen[k] == 'n')
            {
                if (ind_ligne >= 8)
                    throw "Invalid chain";
                p_array[ind_ligne + nbr_slash*width] = Piece("cavalier", false);
                ind_ligne++;
            }
            else if (damier_fen[k] == 'b')
            {
                if (ind_ligne >= 8)
                    throw "Invalid chain";
                p_array[ind_ligne + nbr_slash*width] = Piece("fou", false);
                ind_ligne++;
            }
            else if (damier_fen[k] == 'q')
            {
                if (ind_ligne >= 8)
                    throw "Invalid chain";
                p_array[ind_ligne + nbr_slash*width] = Piece("dame", false);
                ind_ligne++;
            }
            else if (damier_fen[k] == 'k')
            {
                if (ind_ligne >= 8)
                    throw "Invalid chain";
                p_array[ind_ligne + nbr_slash*width] = Piece("roi", false);
                ind_ligne++;
            }
            else if (damier_fen[k] == 'p')
            {
                if (ind_ligne >= 8)
                    throw "Invalid chain";
                p_array[ind_ligne + nbr_slash*width] = Piece("pion", false);
                ind_ligne++;
            }
            else if (damier_fen[k] == 'R')
            {
                if (ind_ligne >= 8)
                    throw "Invalid chain";
                p_array[ind_ligne + nbr_slash*width] = Piece("tour", true);
                ind_ligne++;
            }
            else if (damier_fen[k] == 'N')
            {
                if (ind_ligne >= 8)
                    throw "Invalid chain";
                p_array[ind_ligne + nbr_slash*width] = Piece("cavalier", true);
                ind_ligne++;
            }
            else if (damier_fen[k] == 'B')
            {
                if (ind_ligne >= 8)
                    throw "Invalid chain";
                p_array[ind_ligne + nbr_slash*width] = Piece("fou", true);
                ind_ligne++;
            }
            else if (damier_fen[k] == 'Q')
            {
                if (ind_ligne >= 8)
                    throw "Invalid chain";
                p_array[ind_ligne + nbr_slash*width] = Piece("dame", true);
                ind_ligne++;
            }
            else if (damier_fen[k] == 'K')
            {
                if (ind_ligne >= 8)
                    throw "Invalid chain";
                p_array[ind_ligne + nbr_slash*width] = Piece("roi", true);
                ind_ligne++;
            }
            else if (damier_fen[k] == 'P')
            {
                if (ind_ligne >= 8)
                    throw "Invalid chain";
                p_array[ind_ligne + nbr_slash*width] = Piece("pion", true);
                ind_ligne++;
            }
            else if (isdigit(damier_fen[k]))
            {
                int nbr_vide = int(damier_fen[k]) - '0';
                if (ind_ligne + nbr_vide <= 8) // if we don't go outside of the line of the chessboard
                    for (int l = 0; l < nbr_vide; l++)
                        p_array[ind_ligne + l + nbr_slash*width] = Piece("vide");
                else
                    throw "Invalid chain";
                ind_ligne += nbr_vide;
            }
            else if (damier_fen[k] == ' ')
                nbr_espace++;
            else
                throw "Invalid chain";
        }
        else // we have finished to set the pieces on the chessboard
        {
            if (nbr_slash != 7)
                throw "Invalid chain";
            else
            {
                if (nbr_espace == 1 && !color_found)
                {
                    if (damier_fen[k] == 'w')
                        player_who_play_is_white = true;
                    else if (damier_fen[k] == 'b')
                        player_who_play_is_white = false;
                    else
                        throw "Invalid chain"; 
                    color_found = true; // line reached if and only if we have found a color
                }
                else if (nbr_espace == 2 && !castle_found)
                {
                    int i = 0;
                    string castles = "";
                    while (damier_fen[k+i] != ' ')
                    {
                        castles += damier_fen[k+i];
                        i++;
                    }
                    if (castles == "KQkq")
                        NULL; // we do nothing since initially all the castles are allowed
                    else if (castles == "KQk")
                    {
                        castle_array[3] = false;
                    }
                    else if (castles == "KQq")
                    {
                        castle_array[2] = false;
                    }
                    else if (castles == "Qkq")
                    {
                        castle_array[0] = false;
                    }
                    else if (castles == "KQ")
                    {
                        castle_array[2] = false;
                        castle_array[3] = false;
                    }
                    else if (castles == "Kk")
                    {
                        castle_array[1] = false;
                        castle_array[3] = false;
                    }
                    else if (castles == "Kq")
                    {
                        castle_array[1] = false;
                        castle_array[2] = false;
                    }
                    else if (castles == "Qk")
                    {
                        castle_array[0] = false;
                        castle_array[3] = false;
                    }
                    else if (castles == "Qq")
                    {
                        castle_array[0] = false;
                        castle_array[2] = false;
                    }
                    else if (castles == "kq")
                    {
                        castle_array[0] = false;
                        castle_array[1] = false;
                    }
                    else if (castles == "K")
                    {
                        castle_array[1] = false;
                        castle_array[2] = false;
                        castle_array[3] = false;
                    }
                    else if (castles == "Q")
                    {
                        castle_array[0] = false;
                        castle_array[2] = false;
                        castle_array[3] = false;
                    }
                    else if (castles == "k")
                    {
                        castle_array[0] = false;
                        castle_array[1] = false;
                        castle_array[3] = false;
                    }
                    else if (castles == "q")
                    {
                        castle_array[0] = false;
                        castle_array[1] = false;
                        castle_array[2] = false;
                    }
                    else if (castles == "-")
                    {
                        castle_array[0] = false;
                        castle_array[1] = false;
                        castle_array[2] = false;
                        castle_array[3] = false;
                    }
                    else
                        throw "Invalid chain";
                    castle_found = true;                   
                    k += i - 1; // -1 since the for loop will increase k at the end, whatever it has happened 
                }
                else if (nbr_espace == 3 && !en_passant_found)
                {
                    if (damier_fen[k] == '-')
                        en_passant_found = true;
                    else
                        throw "Invalid chain";
                }
                else if (nbr_espace == 4 && !half_move_found)
                {
                    int i = 0;
                    int h_m = 0;

                    while (damier_fen[k + i] != ' ') {
                        if (isdigit(damier_fen[k + i]))
                            i++;
                        else
                            throw "Invalid chain";
                    }

                    for (int j = 0; j < i; j++) {
                        h_m += (int(damier_fen[k + j]) - '0') * pow(10, i - j - 1);
                       
                    }                   
                    half_move = h_m;
                    half_move_found = true;
                    k += i-1; // -1 since the for loop will increase k at the end, whatever it has happened                    
                }
                else if (nbr_espace == 5 && !full_move_found)
                {
                    int i = 0;
                    int f_m = 0;

                    while (k + i < n && damier_fen[k+i] != ' '){
                        if (isdigit(damier_fen[k]))
                        {                            
                            f_m += (int(damier_fen[k+i]) - '0')*pow(10,n-k-i-1);                            
                            i++;
                        }
                        else
                            throw "Invalid chain";
                    }
                    full_move = f_m;
                    full_move_found = true;
                    k += i-1;                    
                }
                else if (damier_fen[k] == ' ')
                {
                    nbr_espace++;
                }
                else
                    throw "Invalid chain";
            }
        }
    }
    if (!color_found || !castle_found || !en_passant_found || !half_move_found || !full_move_found || nbr_espace != 5)
        throw "Invalid chain";
}


Piece Damier::operator()(const int pos) const{
    if (pos < 0 || pos >= width*length)
        throw out_of_range("0 <= pos < " + to_string(width*length) + " but pos is " + to_string(pos));
    else
        return p_array[pos];
}


void Damier::display() const{
    std::cout << std::flush << std::endl;
    for (int j = 0; j < length; j++)
    {
        for (int i = 0; i < width; i++)
            cout << p_array[i + width*j] << " | ";
        cout << endl;
    }
    cout << endl;
}


void Damier::setPieceOnSquare(const int pos, const Piece p){
    if (pos < 0 || pos >= width*length)
        throw out_of_range("0 <= pos < " + to_string(width*length) + " but pos is " + to_string(pos));
     p_array[pos] = p;
}


bool Damier::isCastle(const bool is_side_left, const bool is_player_white) const{
    //cout << is_side_left << endl;
    if (!is_player_white)
    {
        if (is_side_left)
            return castle_array[0];
        else
            return castle_array[1];
    }
    else
    {
        if (is_side_left)
            return castle_array[2];
        else
            return castle_array[3];
    }
}


void Damier::forbidCastle(const bool is_side_left, const bool is_player_white){
    if (!is_player_white)
    {
        if (is_side_left)
            castle_array[0] = false;
        else
            castle_array[1] = false;
    }
    else
    {
        if (is_side_left)
            castle_array[2] = false;
        else
            castle_array[3] = false;
    }
}


void Damier::allowCastle(const bool is_side_left, const bool is_player_white){
    if (!is_player_white)
    {
        if (is_side_left)
            castle_array[0] = true;
        else
            castle_array[1] = true;
    }
    else
    {
        if (is_side_left)
            castle_array[2] = true;
        else
            castle_array[3] = true;
    }
}


int Damier::getNbrFullMove() const {
    return full_move;
}


bool Damier::getPlayerTurn() const{
    return player_who_play_is_white;
}


bool Damier::isPieceEmpty(const int pos) const{
    if (pos < 0 || pos >= width*length)
            throw out_of_range("0=< pos <" + to_string(width*length) + " or pos vaut " + to_string(pos));
    return (6 == p_array[pos].getId());
}


bool Damier::is_attacked(int* positions, const int nbr_positions, const vector<int>& adv_pos_fin) const{
    for (unsigned int k = 0; k < adv_pos_fin.size(); k++)
        for (int i = 0; i < nbr_positions; i++){
            if (positions[i] < 0 || positions[i] >= width*length)
                throw out_of_range("0 <= all positions < " + to_string(width*length) + " but one of the positions is " + to_string(positions[i]));
            if (adv_pos_fin.at(k) == positions[i])
                return true;
        }
    return false;
}


bool Damier::is_attacked(const int pos, const vector<int> &adv_pos_fin) const{ 
    if (pos < 0 || pos >= width*length)
        throw out_of_range("0 <= pos < " + to_string(width*length) + " but pos is " + to_string(pos));

    for (unsigned int k = 0; k < adv_pos_fin.size(); k++)        
        if (adv_pos_fin.at(k) == pos)
            return true;
    return false;
}


bool Damier::is_king_attacked(const bool is_player_white){
    vector<int> adv_pos_ini_vect;
    vector<int> adv_pos_fin_vect;
    vector<int> adv_promotion_vect;
    bool adv_color = !is_player_white;

    player_possible_movements(adv_color, adv_pos_ini_vect, adv_pos_fin_vect, adv_promotion_vect, false);

    for (int pos = 0; pos < width*length; pos++)
        if (p_array[pos] == Piece(4, is_player_white))
            return is_attacked(pos, adv_pos_fin_vect);
    throw "no king found on the chessboard";
}

const int move_tour[4] = {-10, 10, -1, 1};
void Damier::mvt_tour(const int pos, vector<int> &pos_ini_vect, vector<int> &pos_fin_vect, vector<int> &promotion_vect) const{
    if (pos < 0 || pos >= width*length)
        throw out_of_range("0 <= pos < " + to_string(width*length) + " but pos is " + to_string(pos));

    bool is_player_white = p_array[pos].isWhite();

    for (int k = 0; k < 4; k++)
    {
        int m=1;
        while (true)
        {
            int n = array_120[array_64[pos] + move_tour[k]*m];
            if (n != -1)
            {
                if (isPieceEmpty(n) || p_array[n].isWhite() != is_player_white)
                {
                    push_multiple_elem(pos, pos_ini_vect, n, pos_fin_vect, -1, promotion_vect);
                }
            }
            else
                break;

            if (!isPieceEmpty(n)) // makes sure not to cross the pieces
                break;
            m++;
        }
    }
}


const int move_fou[4] = {-11, -9, 11, 9};
void Damier::mvt_fou(const int pos, vector<int> &pos_ini_vect, vector<int> &pos_fin_vect, vector<int> &promotion_vect) const{
    if (pos < 0 || pos >= width*length)
        throw out_of_range("0 <= pos < " + to_string(width*length) + " but pos is " + to_string(pos));
    bool is_player_white = p_array[pos].isWhite();

    for (int k = 0; k < 4; k++)
    {
        int m=1;
        while (true)
        {
            int n = array_120[array_64[pos] + move_fou[k]*m];
            if (n != -1)
            {
                if (isPieceEmpty(n) || p_array[n].isWhite() != is_player_white)
                {
                    push_multiple_elem(pos, pos_ini_vect, n, pos_fin_vect, -1, promotion_vect);
                }
            }
            else
                break;

            if (!isPieceEmpty(n)) // makes sure not to cross the pieces
                break;
            m++;
        }
    }
}


const int move_cavalier[8] = {-12, -21, -19, -8, 12, 21, 19, 8};
void Damier::mvt_cavalier(const int pos, vector<int> &pos_ini_vect, vector<int> &pos_fin_vect, vector<int> &promotion_vect) const{
    if (pos < 0 || pos >= width*length)
        throw out_of_range("0 <= pos < " + to_string(width*length) + " but pos is " + to_string(pos));
    bool is_player_white = p_array[pos].isWhite();

    for (int k = 0; k < 8; k++)
    {
        int n = array_120[array_64[pos] + move_cavalier[k]];
        if (n != -1)
        {
            if (isPieceEmpty(n) || p_array[n].isWhite() != is_player_white)
            {
                push_multiple_elem(pos, pos_ini_vect, n, pos_fin_vect, -1, promotion_vect);
            }
        }
    }
}


void Damier::mvt_dame(const int pos, vector<int> &pos_ini_vect, vector<int> &pos_fin_vect, vector<int> &promotion_vect) const{
    if (pos < 0 || pos >= width*length)
        throw out_of_range("0 <= pos < " + to_string(width*length) + " but pos is " + to_string(pos));
    mvt_tour(pos, pos_ini_vect, pos_fin_vect, promotion_vect);
    mvt_fou(pos, pos_ini_vect, pos_fin_vect, promotion_vect);
}


const int move_roi[8] = {-11, -10, -9, 1, 11, 10, 9, -1};
void Damier::mvt_roi(const int pos, vector<int>& pos_ini_vect, vector<int>& pos_fin_vect, vector<int>& promotion_vect, const bool callIs_attacked) const{
    if (pos < 0 || pos >= width*length)
        throw out_of_range("0 <= pos < " + to_string(width*length) + " but pos is " + to_string(pos));
    bool is_player_white = p_array[pos].isWhite();
    bool adv_color = !is_player_white;

    vector<int> adv_pos_ini_vect;
    vector<int> adv_pos_fin_vect;
    vector<int> adv_promotion_vect;

    // ==================| Calculation of reachable positions |==================
    for (int k = 0; k < 8; k++)
    {
        int n = array_120[array_64[pos] + move_roi[k]];
        if (n != -1)
        {
            if (isPieceEmpty(n) || p_array[n].isWhite() != is_player_white)
            {
                push_multiple_elem(pos, pos_ini_vect, n, pos_fin_vect, -1, promotion_vect);
            }
        }
    }

    // ==================| Calculation of castle positions, if allowed |==================
    if (callIs_attacked)
    {
        if (is_player_white)
        {
            if (isCastle(false, true) && p_array[h1] == Piece(0, is_player_white)
                    && isPieceEmpty(g1) && isPieceEmpty(f1))
            {
                player_possible_movements(false, adv_pos_ini_vect, adv_pos_fin_vect, adv_promotion_vect, false);
                int* positions = new int[3];
                positions[0] = g1;
                positions[1] = f1;
                positions[2] = pos; // which is e1

                if (!is_attacked(positions, 3, adv_pos_fin_vect))
                    push_multiple_elem(pos, pos_ini_vect, g1, pos_fin_vect, -1, promotion_vect);
                delete[] positions;
            }

            if (isCastle(true, true) && p_array[a1] == Piece(0, is_player_white)
                    && isPieceEmpty(b1) && isPieceEmpty(c1) && isPieceEmpty(d1))
            {
                player_possible_movements(false, adv_pos_ini_vect, adv_pos_fin_vect, adv_promotion_vect, false);
                int* positions = new int[3];
                positions[0] = c1;
                positions[1] = d1;
                positions[2] = pos;

                if (!is_attacked(positions, 3, adv_pos_fin_vect))
                    push_multiple_elem(pos, pos_ini_vect, c1, pos_fin_vect, -1, promotion_vect);
                delete[] positions;
            }
        }

        if (!is_player_white)
        {
            if (isCastle(false, false) && p_array[h8] == Piece(0, is_player_white)
                    && isPieceEmpty(g8) && isPieceEmpty(f8))
            {
                player_possible_movements(true, adv_pos_ini_vect, adv_pos_fin_vect, adv_promotion_vect, false);
                int* positions = new int[3];
                positions[0] = g8;
                positions[1] = f8;
                positions[2] = pos;

                if (!is_attacked(positions, 3, adv_pos_fin_vect))
                    push_multiple_elem(pos, pos_ini_vect, g8, pos_fin_vect, -1, promotion_vect);
                delete[] positions;

            }

            if (isCastle(true, false) && p_array[a8] == Piece(0, is_player_white)
                    && isPieceEmpty(b8) && isPieceEmpty(c8) && isPieceEmpty(d8))
            {
                player_possible_movements(true, adv_pos_ini_vect, adv_pos_fin_vect, adv_promotion_vect, false);
                int* positions = new int[3];
                positions[0] = c8;
                positions[1] = d8;
                positions[2] = pos;

                if (!is_attacked(positions, 3, adv_pos_fin_vect))
                    push_multiple_elem(pos, pos_ini_vect, c8, pos_fin_vect, -1, promotion_vect);
                delete[] positions;
            }
        }
    }
}


void Damier::mvt_pion(const int pos, vector<int>& pos_ini_vect, vector<int>& pos_fin_vect, vector<int>& promotion_vect) const{
    // en-passant moves are not implemented

    if (pos < 0 || pos >= width*length)
        throw out_of_range("0 <= pos < " + to_string(width*length) + " but pos is " + to_string(pos));
    bool is_player_white = p_array[pos].isWhite();

    int i = pos % width;
    int j = (pos - i) / width;    
    // =================| White Pawn |=====================
    if (is_player_white)
    {
        // =============| Square ahead |====================
        int n = array_120[array_64[pos] - 10]; // a white pawn moves straight ahead, hence the -10 in array_64
        if (n != -1)
        {
            if (isPieceEmpty(n))
            {
                if (n < 8) // i.e the pawn is at the top of the chessboard. So, he promotes
                {
                    push_multiple_elem(pos, pos_ini_vect, n, pos_fin_vect, 0, promotion_vect);
                    push_multiple_elem(pos, pos_ini_vect, n, pos_fin_vect, 1, promotion_vect);
                    push_multiple_elem(pos, pos_ini_vect, n, pos_fin_vect, 2, promotion_vect);
                    push_multiple_elem(pos, pos_ini_vect, n, pos_fin_vect, 3, promotion_vect);
                }
                else
                    push_multiple_elem(pos, pos_ini_vect, n, pos_fin_vect, -1, promotion_vect);
            }
        }

        // =============| Second square ahead |====================
        if (j == 6) // i.e. if the pawn is on its origin line
            if (isPieceEmpty(pos-8) && isPieceEmpty(pos-16))
                push_multiple_elem(pos, pos_ini_vect, pos-16, pos_fin_vect, -1, promotion_vect);


        // =============| Capture on the left |====================
        n = array_120[array_64[pos] - 11];
        if (n != -1 && !isPieceEmpty(n) && !p_array[n].isWhite()) 
        {
            if (n < 8) // i.e the pawn is at the top of the chessboard. So, he promotes
            {
                push_multiple_elem(pos, pos_ini_vect, n, pos_fin_vect, 0, promotion_vect);
                push_multiple_elem(pos, pos_ini_vect, n, pos_fin_vect, 1, promotion_vect);
                push_multiple_elem(pos, pos_ini_vect, n, pos_fin_vect, 2, promotion_vect);
                push_multiple_elem(pos, pos_ini_vect, n, pos_fin_vect, 3, promotion_vect);
            }
            else
               push_multiple_elem(pos, pos_ini_vect, n, pos_fin_vect, -1, promotion_vect);
        }

        // =============| Capture on the right |====================
        n = array_120[array_64[pos] - 9];
        if (n != -1 && !isPieceEmpty(n) && !p_array[n].isWhite())
        {
            if (n < 8) // i.e the pawn is at the top of the chessboard. So, he promotes
            {
                push_multiple_elem(pos, pos_ini_vect, n, pos_fin_vect, 0, promotion_vect);
                push_multiple_elem(pos, pos_ini_vect, n, pos_fin_vect, 1, promotion_vect);
                push_multiple_elem(pos, pos_ini_vect, n, pos_fin_vect, 2, promotion_vect);
                push_multiple_elem(pos, pos_ini_vect, n, pos_fin_vect, 3, promotion_vect);
            }
            else
                push_multiple_elem(pos, pos_ini_vect, n, pos_fin_vect, -1, promotion_vect);
        }
    }
    // =================| Black Pawn |=====================
    else
    {
        // =============| Square ahead |====================
        int n = array_120[array_64[pos] + 10]; // a white pawn moves straight ahead, hence the +10 in array_64
        if (n != -1)
        {
            if (isPieceEmpty(n))
            {
                if (n > 55) // i.e the pawn is at the bottom of the chessboard. So, he promotes
                {
                    push_multiple_elem(pos, pos_ini_vect, n, pos_fin_vect, 0, promotion_vect);
                    push_multiple_elem(pos, pos_ini_vect, n, pos_fin_vect, 1, promotion_vect);
                    push_multiple_elem(pos, pos_ini_vect, n, pos_fin_vect, 2, promotion_vect);
                    push_multiple_elem(pos, pos_ini_vect, n, pos_fin_vect,3, promotion_vect);
                }

                else
                    push_multiple_elem(pos, pos_ini_vect, n, pos_fin_vect, -1, promotion_vect);
            }
        }

        // =============| Second square ahead |====================
        if (j == 1) // i.e. if the pawn is on its origin line
            if (isPieceEmpty(pos+8) && isPieceEmpty(pos+16))
                push_multiple_elem(pos, pos_ini_vect, pos+16, pos_fin_vect, -1, promotion_vect);

        // =============| Capture on the left |====================
        n = array_120[array_64[pos] + 9];
        if (n != -1 && !isPieceEmpty(n) && p_array[n].isWhite() ){
            if (n > 55) // i.e the pawn is at the bottom of the chessboard. So, he promotes
            {
                push_multiple_elem(pos, pos_ini_vect, n, pos_fin_vect, 0, promotion_vect);
                push_multiple_elem(pos, pos_ini_vect, n, pos_fin_vect, 1, promotion_vect);
                push_multiple_elem(pos, pos_ini_vect, n, pos_fin_vect, 2, promotion_vect);
                push_multiple_elem(pos, pos_ini_vect, n, pos_fin_vect, 3, promotion_vect);
            }
            else
                push_multiple_elem(pos, pos_ini_vect, n, pos_fin_vect, -1, promotion_vect);
        }

        // =============| Capture on the right |====================
        n = array_120[array_64[pos] + 11];
        if (n != -1 && !isPieceEmpty(n) && p_array[n].isWhite())
        {
            if (n > 55) // i.e the pawn is at the bottom of the chessboard. So, he promotes
            {
                push_multiple_elem(pos, pos_ini_vect, n, pos_fin_vect, 0, promotion_vect);
                push_multiple_elem(pos, pos_ini_vect, n, pos_fin_vect, 1, promotion_vect);
                push_multiple_elem(pos, pos_ini_vect, n, pos_fin_vect, 2, promotion_vect);
                push_multiple_elem(pos, pos_ini_vect, n, pos_fin_vect, 3, promotion_vect);
            }
            else
                push_multiple_elem(pos, pos_ini_vect, n, pos_fin_vect, -1, promotion_vect);
        }
    }
}


void Damier::movement_piece(const int pos, vector<int>& pos_ini_vect, vector<int>& pos_fin_vect, vector<int>& promotion_vect, const bool callIs_attacked) const{
    if (pos < 0 || pos >= width*length)
        throw out_of_range("0 <= pos < " + to_string(width*length) + " but pos is " + to_string(pos));
    int piece_id = p_array[pos].getId();
    switch (piece_id) {
    case 0:
        mvt_tour(pos, pos_ini_vect, pos_fin_vect, promotion_vect);
        break;
    case 1:
        mvt_cavalier(pos, pos_ini_vect, pos_fin_vect, promotion_vect);
        break;
    case 2:
        mvt_fou(pos, pos_ini_vect, pos_fin_vect, promotion_vect);
        break;
    case 3:
        mvt_dame(pos, pos_ini_vect, pos_fin_vect, promotion_vect);
        break;
    case 4:
        mvt_roi(pos, pos_ini_vect, pos_fin_vect, promotion_vect, callIs_attacked);
        break;
    case 5:
        mvt_pion(pos, pos_ini_vect, pos_fin_vect, promotion_vect);
        break;
    }
}


void Damier::player_possible_movements(const bool is_player_white, vector<int>& pos_ini_vect, vector<int>& pos_fin_vect, vector<int>& promotion_vect, const bool callIs_attacked) const{
    for (int j = 0; j < length; j++)
        for (int i = 0; i < width; i++)
            if (!isPieceEmpty(i+width*j) && p_array[i + width*j].isWhite() == is_player_white)
                movement_piece(i + width*j, pos_ini_vect, pos_fin_vect, promotion_vect, callIs_attacked);
}

bool Damier::bouge_piece(const int pos_ini, const int pos_fin, const int promotion){
    if (pos_ini < 0 || pos_ini >= width*length || pos_fin < 0 || pos_fin >= width*length)
        throw out_of_range("0 <= pos_ini AND pos_fin < " + to_string(width*length) + " but pos_ini is " + to_string(pos_ini) + " and pos_fin is " + to_string(pos_fin));
    if (promotion < -1 || promotion > 5)
       throw "Promotion should be superior or equal to -1, and inferior or equal to 5. Its value is " + to_string(promotion);
    //============| Adding castles to the piles of past castles, before the castles were potentially forbidden |=======
    s_castle_lb.push(castle_array[0]); // black left castle
    s_castle_rb.push(castle_array[1]); // black right castle
    s_castle_lw.push(castle_array[2]); // white left castle
    s_castle_rw.push(castle_array[3]); // white right castle

    // ===========| We update the halfmove data before making the moves. |==============
    s_half_move.push(half_move); // we save the value of the half moves for the state of this checkerboard, before making the calculations related to the movement.
    if (p_array[pos_ini].getId() == 5 || p_array[pos_fin].getId() != 6)
    {
        half_move = 0;
    }
    else
        half_move++;    

    //============| cancellation black left castle |==================
    if (isCastle(true, false) && (pos_ini == a8 || pos_ini == e8 || (pos_fin == a8 && p_array[pos_fin] != Piece(0, false)) ))
        //i.e. we moved the left rook or the black king or we ate the black rook
        //normalement, tester si pos_fin est a_8 suffit, car alors cela signifie que la tour vient d'être mangée.
        forbidCastle(true, false);

    //============| cancellation black right castle |=================
    if (isCastle(false, false) && (pos_ini == h8 || pos_ini == e8  || (pos_fin == h8 && p_array[pos_fin] != Piece(0, false)) ))
        //i.e. we moved the right rook or the black king or we ate the black rook
        forbidCastle(false, false);

    //============| cancellation white left castle |==================
    if (isCastle(true, true) && (pos_ini == a1 || pos_ini == e1 || (pos_fin == a1 && p_array[pos_fin] != Piece(0, true)) ))
        //i.e. we moved the left rook or the white king or we ate the white rook
        forbidCastle(true, true);

    //============| cancellation white right castle |=================
    if (isCastle(false, true) && (pos_ini == h1 || pos_ini == e1 || (pos_fin == h1 && p_array[pos_fin] != Piece(0, true)) ))
        //i.e. we moved the right rook or the white king or we ate the white rook
        forbidCastle(false, true);

    //=======================| Data Storage |=========================
    Piece current_piece = p_array[pos_ini];
    bool is_player_white_piece = current_piece.isWhite();
    int id_piece = current_piece.getId();

    int nbr_moves = 0;
    add_move_to_stack(pos_ini, pos_fin, nbr_moves);

    //=====================| general movements |======================
    setPieceOnSquare(pos_fin, current_piece);
    setPieceOnSquare(pos_ini, Piece(6));


    if (pos_ini/width == 1 && id_piece == 5 && is_player_white_piece)
    {
        setPieceOnSquare(pos_fin, Piece(promotion, is_player_white_piece));
    }

    //=====================| Black promotion |========================
    if (pos_ini/width == 6 && id_piece == 5 && !is_player_white_piece)
    {
        setPieceOnSquare(pos_fin, Piece(promotion, is_player_white_piece));
    }

    //============black castles
        //======== left castle
    if (id_piece == 4 && pos_ini == e8 && pos_fin == c8) //pas besoin de vérifier la couleur, seul le roi noir peut faire ce mouvement
    {
        add_move_to_stack(a8, d8, nbr_moves);
        setPieceOnSquare(d8, Piece(0, false));
        setPieceOnSquare(a8, Piece(6)); // erase the old position of the tower        
        forbidCastle(true, false);
    }
        //======== right castle
    if (id_piece == 4 && pos_ini == e8 && pos_fin == g8)
    {
        add_move_to_stack(h8, f8, nbr_moves);
        setPieceOnSquare(f8, Piece(0, false));
        setPieceOnSquare(h8, Piece(6)); // erase the old position of the tower   
        forbidCastle(false, false);
    }

    //============ white castles
        //======== left castle
    if (id_piece == 4 && pos_ini == e1 && pos_fin == c1)
    {
        add_move_to_stack(a1, d1, nbr_moves);
        setPieceOnSquare(d1, Piece(0, true));
        setPieceOnSquare(a1, Piece(6)); // erase the old position of the tower   
        forbidCastle(true, true);
    }
        //======== right_castle
    if (id_piece == 4 && pos_ini == e1 && pos_fin == g1)
    {
        add_move_to_stack(h1, f1, nbr_moves);
        setPieceOnSquare(f1, Piece(0, true));
        setPieceOnSquare(h1, Piece(6)); // erase the old position of the tower
        forbidCastle(false, true);
    }

    s_nbr_elem_back.push(nbr_moves); // we add the number of elements we will have to look at if we want to undo the move.
    
    // ===========| We update the halfmove and fullmove data. |==============
    if (!player_who_play_is_white) //i.e. he is black
        full_move++;   

    // ==========| Before updating the color, we look to see if the move leaves/moves its own king in check. |========
    bool is_valid_move = !is_king_attacked(player_who_play_is_white);

    // =====================| We update the color |==========================
    player_who_play_is_white = !player_who_play_is_white; // it's up to the next player to play

    return is_valid_move;
}


void Damier::add_move_to_stack(const int pos_ini, const int pos_fin, int &nbr_moves){
    if (pos_ini < 0 || pos_ini >= width*length || pos_fin < 0 || pos_fin >= width*length)
        throw out_of_range("0 <= pos_ini AND pos_fin < " + to_string(width*length) + " but pos_ini is " + to_string(pos_ini) + " and pos_fin is " + to_string(pos_fin));

    s_pos_ini.push(pos_ini);
    s_piece_moved.push(p_array[pos_ini]);
    s_pos_fin.push(pos_fin);
    s_piece_erased.push(p_array[pos_fin]);
    nbr_moves++;
}


void Damier::undo_move(){
    // ============| Cancellation of pieces' movements |=================    
    for (int k = 0; k < s_nbr_elem_back.top(); k++)
    {
        p_array[s_pos_ini.top()] = s_piece_moved.top();
        p_array[s_pos_fin.top()] = s_piece_erased.top();        

        s_pos_ini.pop();
        s_pos_fin.pop();
        s_piece_moved.pop();
        s_piece_erased.pop();        
    }
    s_nbr_elem_back.pop();

    // =================| Post Stack Processing |===============
    player_who_play_is_white = !player_who_play_is_white; // we cancel the color change, to say that it's up to the former player to play
    if (!player_who_play_is_white) // if it was the black that moved, we decrease full_move
        full_move--; // castling is considered as a single movement

    //============| Back in time of the halfmoves |============
    half_move = s_half_move.top();
    s_half_move.pop();

    //============| Back in time of the castles|============
    castle_array[0] = s_castle_lb.top();
    s_castle_lb.pop();
    castle_array[1] = s_castle_rb.top();
    s_castle_rb.pop();
    castle_array[2] = s_castle_lw.top();
    s_castle_lw.pop();
    castle_array[3] = s_castle_rw.top();
    s_castle_rw.pop();

}


string Damier::generateFEN(){
    string fen_format = "";    
    for (int j = 0; j < length; j++)
    {
        int nbr_void = 0;
        for (int i = 0; i < width; i++)
        {
            if (p_array[i + width*j].getId() == 6)
                nbr_void++;
            else
            {
                if (nbr_void != 0)
                {
                    fen_format += to_string(nbr_void);
                    nbr_void = 0;
                }
                Piece piece = p_array[i + width*j];

                if (piece == Piece(0, true))
                    fen_format += "R";
                else if (piece == Piece("cavalier", true))
                    fen_format += "N";
                else if (piece == Piece("fou", true))
                    fen_format += "B";
                else if (piece == Piece("dame", true))
                    fen_format += "Q";
                else if (piece == Piece("roi", true))
                    fen_format += "K";
                else if (piece == Piece("pion", true))
                    fen_format += "P";
                else if (piece == Piece("tour", false))
                    fen_format += "r";
                else if (piece == Piece("cavalier", false))
                    fen_format += "n";
                else if (piece == Piece("fou", false))
                    fen_format += "b";
                else if (piece == Piece("dame", false))
                    fen_format += "q";
                else if (piece == Piece("roi", false))
                    fen_format += "k";
                else if (piece == Piece("pion", false))
                    fen_format += "p";
                else
                    throw "unknown piece found";
            }
        }
        if (nbr_void != 0)
            fen_format += to_string(nbr_void);
        if (j < length - 1)
            fen_format += "/";
    }
    // ================| Addition of color indication |==================
    if (player_who_play_is_white)
        fen_format += " w ";
    else
        fen_format += " b ";
    // ================| Addition of the indication of the castles |==================

    bool at_least_one_castle = std::any_of(std::begin(castle_array), std::end(castle_array), [&](bool boolean)
    {
        return boolean == true;
    });

    if (at_least_one_castle) // the front space is managed in color
    {
        if (isCastle(false, true))
            fen_format += "K";
        if (isCastle(true, true))
            fen_format += "Q";
        if (isCastle(false, false))
            fen_format += "k";
        if (isCastle(true, false))
            fen_format += "q";
    }
    else
        fen_format += "-";

    // =============| You don't treat en-passant moves|================
    fen_format += " -";
    // ================| Addition of halfmoves |==================
    fen_format += " " + to_string(half_move);
    // ================| Addition of fullmoves |==================
    fen_format += " " + to_string(full_move);

    return fen_format;
}


void push_multiple_elem(const int& v1, vector<int>& vect1, const int& v2, vector<int>& vect2, const int v3, vector<int>& vect3){
    vect1.push_back(v1);
    vect2.push_back(v2);
    vect3.push_back(v3);
}
