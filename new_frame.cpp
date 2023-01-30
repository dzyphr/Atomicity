#include <bits/stdc++.h>
using std::cout, std::string, std::endl;
int main(int argc, char* argv[])
{
	if (argc < 2)
	{
		cout << "enter the name of the new contract frame to create";
	}
	else
	{
		string newFrameName = argv[1];
		string command = "cp -r basic_framework " + newFrameName;
		const char* c_cmd = command.c_str();
		system(c_cmd);
		string newContract = "echo \'// SPDX-License-Identifier: GPL-3.0-only\npragma solidity >=0.8.0 <0.9.0;\n\ncontract "+ newFrameName +"\n{\n\n}\' > " + newFrameName + "/contracts/" + newFrameName + ".sol";
		const char* c_newContract = newContract.c_str();
		system(c_newContract);
	}
}
