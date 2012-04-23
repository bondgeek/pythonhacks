
clean:
	find quantlib -name \*.so -exec rm {} \;
	find quantlib -name \*.pyc -exec rm {} \;
	find quantlib/time -name \*.cpp -exec rm {} \;
	find quantlib/instruments -name \*.cpp -exec rm {} \;
	find quantlib/examples -name \*.cpp -exec rm {} \;
	find quantlib/indexes -name \*.cpp -exec rm {} \;
	find quantlib/math -name \*.cpp -exec rm {} \;
	find quantlib/models/equity -name \*.cpp -exec rm {} \;
	find quantlib/pricingengines -name \*.cpp -exec rm {} \;
	find quantlib/processes -name \*.cpp -exec rm {} \;
	find quantlib/settings -name \settings.cpp -exec rm {} \;
	find quantlib/sim -name \simulate.cpp -exec rm {} \;
	find quantlib/test -name \test_cython_bug.cpp -exec rm {} \;
	find quantlib/termstructures/yields -name \flat_forward.cpp -exec rm {} \;
	find quantlib/termstructures/yields -name \rate_helpers.cpp -exec rm {} \;
	find quantlib/termstructures/yields -name \zero_curve.cpp -exec rm {} \;
	find quantlib/termstructures/yields -name \yield_termstructure.cpp -exec rm {} \;
	find quantlib/termstructures/volatility/equityfx -name \*.cpp -exec rm {} \;
	rm -rf quantlib/*.cpp
	rm -rf build
	rm -rf dist
docs:
	make -C docs html


build:
	python setup.py build_ext --inplace

build2:
#	find quantlib/instruments -name \swaps.cpp -exec rm {} \;
#	find quantlib/instruments -name \bonds.cpp -exec rm {} \;
	python setup2.py build_ext --inplace
    
test:
	nosetests -v quantlib/test
