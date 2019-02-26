#include <iostream>
#include <memory>
#include <thread>
#include <atomic>
#include <chrono>
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
	double currentPeriod = period;
	while(1){
		task(nTaskCalls, calc);
		timer.sleepUntil(currentPeriod);
		currentPeriod += period;
	}
	cerr << "nTaskCalls: " << nTaskCalls << endl;
	cerr << "calc: " << calc << endl;
	return 0;
}
