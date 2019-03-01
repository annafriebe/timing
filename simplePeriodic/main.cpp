#include <iostream>
#include <memory>
#include <thread>
#include <atomic>
#include <chrono>
#include <pthread.h>
#include "Timer.h"

const double period = 0.01;
using namespace std;

namespace{
	void task(int& nPeriod, double& calc){
		for(int i=1; i<=100; ++i){
			calc +=nPeriod%i;
		}
		nPeriod++;
	}
}

int main(int argc, char *argv[]) {
	Timer timer;
	int nTaskCalls = 0;
	double calc = 0;
	timer.start();
	int nPeriods = 1;
	double currentPeriod = period;
	pthread_attr_t attr;
	pthread_attr_init(&attr);
	if(pthread_attr_setschedpolicy(&attr, SCHED_RR) != 0){
		fprintf(stderr, "Unable to set policy.\n");
	}

	while(1){
		task(nTaskCalls, calc);
		timer.sleepUntil(currentPeriod);
		currentPeriod = ++nPeriods * period;
	}
	cerr << "nTaskCalls: " << nTaskCalls << endl;
	cerr << "calc: " << calc << endl;
	return 0;
}
