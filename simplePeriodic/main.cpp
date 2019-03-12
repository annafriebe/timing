#include <iostream>
#include <memory>
#include <thread>
#include <atomic>
#include <chrono>
#include <functional>
#include <stdlib.h>
#include <pthread.h>
#include "Timer.h"

const double period = 0.01;
using namespace std;

namespace{
	hash<int> intHash;	
	void task(int& nPeriod, array<size_t, 100>& calcValues){
		for(auto& val : calcValues){
			val = intHash(val);
		}
		nPeriod++;
	}
}

int main(int argc, char *argv[]) {
	Timer timer;
	array<size_t, 100> calcValues;
	timer.start();
	int nPeriods = 0;
	double currentPeriod = 0;
	pthread_attr_t attr;
	pthread_attr_init(&attr);
	// set scheduling policy
	if(pthread_attr_setschedpolicy(&attr, SCHED_RR) != 0){
		fprintf(stderr, "Unable to set policy.\n");
	}
	// set up random starting values
	for(auto& val : calcValues){
		val = rand();
	}

	while(1){
		task(nPeriods, calcValues);
		currentPeriod = nPeriods * period;
		timer.sleepUntil(currentPeriod);
	}
	cerr << "nPeriods: " << nPeriods << endl;
	for(const int& val:calcValues){
		cerr << val << endl; 
	}
	return 0;
}
