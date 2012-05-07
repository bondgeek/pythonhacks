#include <_dateparser.hpp>
#include <stdio.h>

namespace DP 
{
    int year(int date) {
        char *buf ;
        
        boost::regex pat("(?<Y>[1-9][0-9]{3})(?<M>[0-1][0-9])(?<D>[0-3][0-9])");
        
        std::sprintf(buf, "%d", date);
        
        return 0;
    }
}