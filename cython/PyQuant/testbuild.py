# Basic build tests

def test_import1():
    try:
        import quantlib 
        print("Testing version: %s" % quantlib.version.get_version())
    except ImportError:
        print("\nQuantlib Module Not Found!\n")
        return False
    except:
        return False
    else:
        print("\nImport successful")
        
    return True

def test_import_daycounters():
    try:
        from quantlib.time.daycounter import (
            Actual360, DayCounter, SimpleDayCounter
        )
        
        from quantlib.time.daycounters.actual_actual import (
            ActualActual, ISDA, ISMA, AFB
        )
        
        from quantlib.time.daycounters.thirty360 import (
                Thirty360, EUROBONDBASIS
        )
        from quantlib.time.date import (
            Date, November, May, February, July, January, Period,
            Months
        )
        
    except ImportError:
        print("\nA Quantlib DayCounter Module Was Not Found!\n")
        return False
    else:
        print("\nDay Counter Import successful")
    return True

def test_quotes():
    try:
        from quantlib.quotes import SimpleQuote
    except:
        print("\nProblem importing SimpleQuote")
        return False

    try:
        assert SimpleQuote(666).value == 666.0
    except:
        print("SimpleQuote test failed")
        return False
    else:
        print("SimpleQuote success")
    
    return True


if __name__ == "__main__":
    
    test_quotes()
    print("\nEND\n")
