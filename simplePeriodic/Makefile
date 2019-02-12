#######################################################
#
#    C++-kurs, laboration 1, test
#    -------------------------------------------
#
#######################################################

CC = g++ 
FLAGS = -Wall -pedantic -Werror -std=c++17 -pthread

SOURCES = Timer.cpp
MAIN = main.cpp

HEADERS = Timer.h
FILE = simplePeriodic
MAKE = make

.PHONY : 

all : $(FILE)

debug : FLAGS += -DDEBUG -g
debug: $(FILE)

clean :
	rm -f $(FILE)
	rm -f $(TEST_FILE)
	rm -rf *.o	


$(FILE) : $(SOURCES) $(HEADERS) $(MAIN)
	$(CC) $(SOURCES) $(MAIN) $(FLAGS) -o $(FILE)

