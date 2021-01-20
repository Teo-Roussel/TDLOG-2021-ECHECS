#ifndef PIECE_H
#define PIECE_H



#include <map>
#include <vector>
#include <iostream>
using namespace std;

static std::string const name_array[7] = {"tour", "cavalier", "fou", "dame", "roi", "pion", "vide"};
// a piece (without color) is defined by its id
// an empty square is a "vide" piece


std::map<string, int> init_mapOfValues();
static const std::map<std::string, int> mapOfValues = init_mapOfValues();

std::map<int, int> init_mapOfValues_();
static const std::map<int, int> mapOfValues_ = init_mapOfValues_();


class Piece{
    int id;
    bool is_white;

public:
    /**
     * @brief Piece : construct a Piece 'vide', with is_white set to 'false'.
     */
    Piece();

    /**
     * @brief Piece : constructor of a Piece with initial id 'piece_id' and of color 'player_color'
     * @param piece_id : an int between 0 and 6
     * @param player_color : a boolean which explains if the piece is white or black
     */
    Piece(const int piece_id, const bool player_color = false);

    /**
     * @brief Piece : construct a piece according to a name and a boolean which corresponds to the color
     * @param name : a string which is the name of the piece
     * @param player_color : true if white, false otherwise.
     * @throw a char* if the name if not accepted.
     */
    Piece(const string name, const bool player_color = false);

    /**
     * @brief getName : return the name of the Piece
     * @return the name of the Piece
     */
    std::string getName() const;

    /**
     * @brief isWhite : return a boolean which shows if the Piece is white (false if the piece is empty)
     * @return a boolean
     */
    bool isWhite() const;

    /**
     * @brief getId : return the id of the Piece
     * @return the id of the Piece
     */
    int getId() const;


    bool operator==(const Piece& piece) const;
    bool operator!=(const Piece& piece) const;
    friend std::ostream & operator << (std::ostream &out, const Piece &piece);
};

std::ostream & operator<<(std::ostream &out, const Piece &obj);

#endif // PIECE_H
