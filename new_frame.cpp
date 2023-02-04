#include <bits/stdc++.h>
#include <vector>
using std::cout, std::string, std::endl, std::vector;
void standardOperations(string arg1);
void extraArgCheck(int argc, char* argv[]);
void arg2IsMultiFile(int argc, char* argv[]);
void arg2IsConstructorArgs(int argc, char* argv[]);
int main(int argc, char* argv[])
{
	if (argc < 2)
	{
		cout << "enter the name of the new contract frame to create\n";
	}
	else if (argc >= 2)
	{

		standardOperations(argv[1]);
		if (argc > 2)
		{
			extraArgCheck(argc, argv);
		}
	}
}

void standardOperations(string arg1)
{
	string newFrameName = arg1;
	string command = "mkdir " + newFrameName + " && cp -r basic_framework/* " + newFrameName + "/";
	system(command.c_str());
	string newContract = "echo \'// SPDX-License-Identifier: GPL-3.0-only\npragma solidity >=0.8.0 <0.9.0;\n\ncontract "+ newFrameName +"\n{\n\n}\' > " + newFrameName + "/contracts/" + newFrameName + ".sol";
	system(newContract.c_str());
	string echoName = "echo \'ContractName=\"" + newFrameName  + "\"' >> " + newFrameName + "/.env";
	system(echoName.c_str());

}

void extraArgCheck(int argc, char* argv[])
{
	string newFrameName = argv[1];
	if (argc >= 3)
	{
		string newFrameName = argv[1];
		string arg2 = argv[2];
		if (arg2 == "-M")
		{
			arg2IsMultiFile(argc, argv);
		}
		else if (arg2 == "-CA")
		{
			arg2IsConstructorArgs(argc, argv);
		}
		else
		{
			//arg2 is not -CA or -M which currently means we have an unrecognized argument
			cout << "unrecognized command: " << arg2;
			exit(1);
		}
	}
	else
	{
		string echoMultiFileFalse = "echo \'MultiFile=\"False\"\' >> " + newFrameName + "/.env";
		string echoContructorArgsFalse = "echo \'ConstructorArgs=\"False\"\' >> " + newFrameName + "/.env";
		system(echoMultiFileFalse.c_str());
		system(echoContructorArgsFalse.c_str());
	}
}

void arg2IsMultiFile(int argc, char* argv[])
{
	string newFrameName = argv[1];
	string echoFlatten = 
		"echo \'{\"inputFilePath\": \"../" + 
		newFrameName  + "/contracts/" + 
		newFrameName  + ".sol\",\"outputDir\": \"../" + 
		newFrameName  + "/contracts/\"}\' > solidity-flattener/config.json";
	system(echoFlatten.c_str());
	string echoMultiFileTrue = "echo \'MultiFile=\"True\"\' >> " + newFrameName + "/.env";
	system(echoMultiFileTrue.c_str());
	if (argc >= 4)
	{
		if (argc >= 5)
		{
			string cacheck = argv[3];
			if (cacheck == "-CA")
			{
				string echoContructorArgsTrue = "echo \'ConstructorArgs=\"True\"\' >> " + newFrameName + "/.env";
				system(echoContructorArgsTrue.c_str());
				string str_dec = argv[4];
				string::size_type size;
				int constructorArgCount = std::stoi(str_dec, &size);
				vector<string> argumentVector;
				int argumentIndex = 5;
				string pyFmtArgArray = "constructorParamVals = [";
				if (argc >= argumentIndex + constructorArgCount)
				{
					for (int i = 0; i < constructorArgCount; i++)
					{
						argumentVector.push_back(argv[argumentIndex + i]);
					}
					int i =0;
					for (auto const& value : argumentVector)
					{
					//	cout << value << '\n';
						pyFmtArgArray = pyFmtArgArray + value;
					       	if (i != argumentVector.size()-1)
						{
							pyFmtArgArray = pyFmtArgArray + ',';
						}	
						i = i + 1;
					}
					pyFmtArgArray = pyFmtArgArray + ']';
					string pyEchoArgArray = "echo \'" + pyFmtArgArray + "\' | cat - " + newFrameName  + "/py/deploy.py > pyFmtArgsTEMP && mv pyFmtArgsTEMP " + newFrameName + "/py/deploy.py";
		                        system(pyEchoArgArray.c_str());

					//cout << pyFmtArgArray << '\n';
				}
				else
				{
					cout << "Number of constructor args exceeds provided values for those arguments!\n";
					exit(1);
				}

			}
			else
			{
				cout << "unrecognized command: " << argv[3] << '\n';
				exit(1);
			}
		}
		else
		{
			cout << "-CA flag used without providing count of constructor args, provide them as next arg!\n";
			exit(1);
		}
	}
	else
	{
		string echoContructorArgsFalse = "echo \'ConstructorArgs=\"False\"\' >> " + newFrameName + "/.env";
		system(echoContructorArgsFalse.c_str());

	}
}

void arg2IsConstructorArgs(int argc, char* argv[])
{
	string newFrameName = argv[1];
	string echoContructorArgsTrue = "echo \'ConstructorArgs=\"True\"\' >> " + newFrameName + "/.env";
	system(echoContructorArgsTrue.c_str());
	if (argc >= 4)
	{
		string str_dec = argv[3];
		string::size_type size;
		int constructorArgCount = std::stoi(str_dec, &size);
		vector<string> argumentVector;
		int argumentIndex = 4;
		string pyFmtArgArray = "constructorParamVals = [";
		if (argc >= argumentIndex + constructorArgCount)
		{
			for (int i = 0; i < constructorArgCount; i++)
			{
				argumentVector.push_back(argv[argumentIndex + i]);
			}
			int i = 0;
			for (auto const& value : argumentVector)
			{
				//cout << value << '\n';
				pyFmtArgArray = pyFmtArgArray + value;
				if (i != argumentVector.size()-1)
				{
					pyFmtArgArray = pyFmtArgArray + ',';
				}
				i = i + 1;

			}
			pyFmtArgArray = pyFmtArgArray + ']';
			string pyEchoArgArray = "echo \'" + pyFmtArgArray + "\' | cat - " + newFrameName  + "/py/deploy.py > pyFmtArgsTEMP && mv pyFmtArgsTEMP " + newFrameName + "/py/deploy.py";
			system(pyEchoArgArray.c_str());
			//cout << pyFmtArgArray << '\n';
		}
		else
		{
			cout << "Number of constructor args exceeds provided values for those arguments!\n";
			exit(1);
		}
		if (argc > argumentIndex + constructorArgCount)
		{
			string currentArg = argv[argumentIndex + constructorArgCount];
			if (currentArg == "-M")
			{
				string echoMultiFileTrue = "echo \'MultiFile=\"True\"\' >> " + newFrameName + "/.env";
				system(echoMultiFileTrue.c_str());
				string echoFlatten = 
					"echo \'{\"inputFilePath\": \"../" + 
					newFrameName  + "/contracts/" + 
					newFrameName  + ".sol\",\"outputDir\": \"../" + 
					newFrameName  + "/contracts/\"}\' > solidity-flattener/config.json";
				system(echoFlatten.c_str());
			}
			else
			{
				cout << "unrecognized command: " << argv[argumentIndex + constructorArgCount] << '\n';
				exit(1);
			}
		}
		else
		{
			string echoMultiFileFalse = "echo \'MultiFile=\"False\"\' >> " + newFrameName + "/.env";
			system(echoMultiFileFalse.c_str());
		}
	}
	else
	{
		cout << "-CA flag used without providing count of constructor args, provide them as next arg!\n";
		exit(1);
	}
}
