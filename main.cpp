#include <iostream>
#include <memory>
#include <thread>
#include <atomic>
#include <chrono>
#include "Timer.h"

const double period = 0.01;

namespace{
	void task(int& nPeriods){
		nPeriods++;
	}
}

int main(int argc, char *argv[]) {
	Timer timer;
	int nPeriod = 0;
	timer.start();
	while(1){
		task(nPeriod);
		timer.sleepUntil(period);
		timer.reset();
	}
	return 0;
}
