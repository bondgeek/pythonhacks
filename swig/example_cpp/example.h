// example.h
#include <algorithm>

namespace bm 
{

using namespace std;
class Pos
{
public:
    float x, y;
    Pos() : x(0), y(0) {}
    Pos(float x, float y) : x(x), y(y) {}
    Pos operator+(const Pos& b) const { return Pos(x+b.x, y+b.y); }
    Pos operator-(const Pos& b) const { return Pos(x-b.x, y-b.y); }
    Pos operator*(const Pos& b) const { return Pos(x*b.x, y*b.y); }
    Pos operator/(const Pos& b) const { return Pos(x/b.x, y/b.y); }
    static Pos create_from_min(const Pos& a, const Pos& b) { return Pos(min(a.x,b.x), min(a.y,b.y)); }
    static Pos create_from_max(const Pos& a, const Pos& b) { return Pos(max(a.x,b.x), max(a.y,b.y)); }
};

int increment(int x);
}