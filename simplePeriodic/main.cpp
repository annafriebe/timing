#include <iostream>
#include <thread>
#include <chrono>
#include <pthread.h>
#include <sched.h>

using namespace std;

namespace{
	const chrono::milliseconds periodDuration(10);
	const int moduloVal = 4711;
	const int addVal = 47;
	void task(int& nPeriod, array<int, 100>& calcValues) noexcept {
		for(auto& val : calcValues){
			val = (val + addVal)%moduloVal;
		}
		nPeriod++;
	}
}

int main(int argc, char *argv[]) {
	array<int, 100> calcValues;
	int nPeriods = 0;
	pthread_t this_thread = pthread_self();
	struct sched_param params;
	params.sched_priority = sched_get_priority_max(SCHED_RR);
	int ret = pthread_setschedparam(this_thread, SCHED_RR, &params);
    if (ret != 0) {
		cerr << "Unable to set scheduling parameters." << endl;
	}
	else {
		cerr << "Scheduling parameters properly set." << endl;
	}
	int policy = 0;
    ret = pthread_getschedparam(this_thread, &policy, &params);
    if (ret != 0) {
        cerr << "Couldn't retrieve real-time scheduling paramers" << endl;
		return 0;
    }
 
    // Check the correct policy was applied
    if(policy != SCHED_RR) {
       cerr << "Scheduling is NOT SCHED_RR!" << std::endl;
    } else {
        cerr << "SCHED_RR OK" << endl;
    }
 
    // Print thread scheduling priority
    cerr << "Thread priority is " << params.sched_priority << endl; 

	// set up random starting values
	for(auto& val : calcValues){
		val = rand()%moduloVal;
	}
	std::chrono::steady_clock::time_point next = 
		chrono::steady_clock::now();	

	while(1){
		task(nPeriods, calcValues);
		next += periodDuration;
		std::this_thread::sleep_until(next);
	}
	cerr << "nPeriods: " << nPeriods << endl;
	for(const int& val:calcValues){
		cerr << val << endl; 
	}
	return 0;
}
