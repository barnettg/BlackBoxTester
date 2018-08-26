def example(*args, **kwargs):
    print(str(args))
    print(str(kwargs))

def example2(arg1="default_arg1",*, param1="default1", param2="default2"):
    print(arg1)
    print(param1)
    print(param2)

def example3(arg1="default_arg1",*, param1="default1", param2="default2", **kwargs):
    print(arg1)
    print(param1)
    print(param2)
    print(str(kwargs))

example("arg1", param1="param1_data",param2="param2_data" )
example2("arg1", param1="param1_data" )
example2("arg1", param1="param1_data",param2="param2_data" )

example3(arg1="arg1", param1="param1_data",param2="param2_data", param3="blah" )
