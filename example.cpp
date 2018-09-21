/*
This is a sample program to illustrate argument passing in C++ and enable the
run.sh script to compile and run a program.
*/
#include <iostream>

using namespace std;

int main(int argc, char* argv[])
{
	if(argc == 2)
	{
		cout << "The config file passed is: " << argv[1] << endl;

	}else
	{
		cout << "Refering to a default case because there were no arguments passed!" << endl;
	}

	return 0;
}