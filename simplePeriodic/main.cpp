#include <iostream>
#include <memory>
#include <thread>
#include <atomic>
#include <chrono>
#include <functional>
#include <pthread.h>
#include "Timer.h"

using namespace std;

namespace{
	const double period = 0.01;
	const int moduloVal = 4711;
	const int addVal = 47;
	void task(int& nPeriod, array<int, 100>& calcValues){
		for(auto& val : calcValues){
			val = (val + addVal)%moduloVal;
		}
		nPeriod++;
	}
}

int main(int argc, char *argv[]) {
	Timer timer;
	array<int, 100> calcValues;
	timer.start();
	int nPeriods = 0;
	double currentPeriod = 0;
	pthread_attr_t attr;
	pthread_attr_init(&attr);
	// set scheduling policy
	if(pthread_attr_setschedpolicy(&attr, SCHED_RR) != 0){
		cerr << "Unable to set policy." << endl;
	}
	int policy;
	pthread_attr_getschedpolicy(&attr, &policy);
	if(policy == SCHED_RR){
		cerr << "Policy properly set" << endl;
	}
	// set up random starting values
	for(auto& val : calcValues){
		val = rand()%moduloVal;
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
