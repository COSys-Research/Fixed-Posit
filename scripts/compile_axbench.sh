cd blackscholes/src
g++ -march=nehalem -Wall -Wnarrowing -lboost_regex -std=c++11 -O3 blackscholes.c -o blackscholes.out

cd ../../fft/src
g++ -march=nehalem -Wall -lboost_regex -std=c++11 -c complex.cpp -o complex.o
g++ -march=nehalem -Wall -lboost_regex -std=c++11 -c fourier.cpp -o fourier.o
g++ -march=nehalem -Wall -lboost_regex -std=c++11 -c fft.cpp -o fft.o
g++ -march=nehalem -Wall -lboost_regex fourier.o complex.o fft.o -o fft.out

cd ../../inversek2j/src
g++ -march=nehalem -Wall -lboost_regex -std=c++11 -c kinematics.cpp -o kinematics.o
g++ -march=nehalem -Wall -lboost_regex -std=c++11 -c inversek2j.cpp -o inversek2j.o
g++ -march=nehalem -Wall -lboost_regex kinematics.o inversek2j.o -o inversek2j.out

cd ../../jmeint/src
g++ -march=nehalem -Wall -lboost_regex -std=c++11 -c tritri.cpp -o tritri.o
g++ -march=nehalem -Wall -lboost_regex -std=c++11 -c jmeint.cpp -o jmeint.o
g++ -march=nehalem -Wall -lboost_regex tritri.o jmeint.o -o jmeint.out

cd ../../jpeg/src
g++ -march=nehalem -Wall -lboost_regex -std=c++11 -c rgbimage.c -o rgbimage.o
g++ -march=nehalem -Wall -lboost_regex -std=c++11 -c quant.c -o quant.o
g++ -march=nehalem -Wall -lboost_regex -std=c++11 -c marker.c -o marker.o
g++ -march=nehalem -Wall -lboost_regex -std=c++11 -c jpeg.c -o jpeg.o
g++ -march=nehalem -Wall -lboost_regex -std=c++11 -c huffman.c -o huffman.o
g++ -march=nehalem -Wall -lboost_regex -std=c++11 -c encoder.c -o encoder.o
g++ -march=nehalem -Wall -lboost_regex -std=c++11 -c dct.c -o dct.o
g++ -march=nehalem -Wall -lboost_regex rgbimage.o quant.o marker.o jpeg.o huffman.o encoder.o dct.o -o jpeg.out

cd ../../kmeans/src
g++ -march=nehalem -Wall -lboost_regex -std=c++11 -fPIC -c rgbimage.c -o rgbimage.o
g++ -march=nehalem -Wall -lboost_regex -std=c++11 -fPIC -c distance.c -o distance.o
g++ -march=nehalem -Wall -lboost_regex -std=c++11 -fPIC -c segmentation.c -o segmentation.o
g++ -march=nehalem -Wall -lboost_regex -std=c++11 -fPIC -c kmeans.c -o kmeans.o
g++ -march=nehalem -Wall -lboost_regex -std=c++11 -fPIC kmeans.o rgbimage.o distance.o segmentation.o -o kmeans.out
