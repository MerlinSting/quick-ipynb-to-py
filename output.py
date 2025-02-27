
# # Markdown Cell:
# This is a test notebook.
# It contains code and markdown cells.
# We will use it to test the ipynb to py converter.


a = 10
b = 20
c = (a + b)
print(c)




def my_function(x, y):

    '\n    This is a test function.\n    '
    result = (x * y)
    return result
result1 = my_function(5, 6)
print(result1)




class MyClass():


    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value
obj = MyClass(42)
print(obj.get_value())



used_variable = 50
print(used_variable)



for i in range(3):
    temp_var = (i * 2)
    print(temp_var)


 Code Cell 6:

def another_function(p, q):

    return p + q

result2 = another_function(1, 2)
print(result2)

#Code Cell 7:
test_list = [1,2,3,4,5]
for item in test_list:
    print(item)

#Code Cell 8:
test_dict = {"a":1, "b":2}
print(test_dict["a"])

#Code Cell 9:
#this should produce a syntax error if not handled.
#for i in range(3):
# print(i)

#Code Cell 10:

def function_with_type_hint(value: int) -> str:

    return str(value)

print(function_with_type_hint(123))
