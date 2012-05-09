#include <_dateparser.hpp>

namespace DP 
{

    std::string year(std::string datestr) {
        boost::smatch matches;
        
        boost::regex pat("(?<Y>[1-9][0-9]{3})(?<M>[0-1][0-9])(?<D>[0-3][0-9])");  
              
        if (boost::regex_match(datestr, matches, pat)) 
        {
            return matches["Y"] ;
        }
        return "";
    }
}
