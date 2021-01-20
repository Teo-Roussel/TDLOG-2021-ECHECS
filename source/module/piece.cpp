#include "piece.h"

map<string, int> init_mapOfValues() {
    std::map<std::string, int> map;
    map.insert(std::make_pair("vide", 0));
    map.insert(std::make_pair("roi", 20000));
    map.insert(std::make_pair("dame", 900));
    map.insert(std::make_pair("tour", 500));
    map.insert(std::make_pair("cavalier", 320));
    map.insert(std::make_pair("fou", 330));
    map.insert(std::make_pair("pion", 100));
    return map;
}


map<int, int> init_mapOfValues_() {
    std::map<int, int> map;
    map.insert(std::make_pair(6, 0));
    map.insert(std::make_pair(4, 20000));
    map.insert(std::make_pair(3, 900));
    map.insert(std::make_pair(0, 500));
    map.insert(std::make_pair(1, 320));
    map.insert(std::make_pair(2, 330));
    map.insert(std::make_pair(5, 100));
    return map;
}


// ===========| Empty constructor |=============
Piece::Piece(){
    id = 6;
    is_white = false;
    // the piece is not white, since she is empty
    // to know if a piece is black or white, we can't limit a test on a piece 
    // to a test on the boolean 'is_white'. We have also to know if the piece is non empty    
}


Piece::Piece(int piece_id, bool player_color){
    if (piece_id < 0 || piece_id > 6)
        throw "piece_id should verify :  0 <= piece_id <= 6";
    id = piece_id;
    is_white = player_color;
}


Piece::Piece(string name, bool player_color){
    is_white = player_color;
    bool id_found = false;
    for (int i=0; i<7 && !id_found; i++)
        if (name_array[i] == name) {
            id = i;
            id_found = true;
        }
    if (!id_found)
        throw "the name is not correct";
}


string Piece::getName() const {
    return name_array[id];
}


bool Piece::isWhite() const{return is_white;}


int Piece::getId() const {return id;}


bool Piece::operator==(const Piece& piece) const{
    return (id == piece.id && is_white== piece.is_white);
}


bool Piece::operator!=(const Piece& piece) const{
    return (id != piece.id || is_white != piece.is_white);
}


std::string const name_array_affichage[7] = {"tour", "cava", "fou ", "dame", "roi ", "pion", "vide"};

std::ostream & operator<<(std::ostream &os, const Piece &piece)
{
    os << ((piece.id == 6) ? "     v    " : (piece.is_white ? ( name_array_affichage[piece.getId()] + " Blanc" ): (name_array_affichage[piece.getId()] + "  Noir")));
    return os;
}
