# Programs.
# Small snippets
# pythn  


# def Pyramid():
#     # rows = int(input("Enter the number of rows: "))
#     rows = 8
#     for i in range(rows, 0, -1):
#         left = "*" * i

#         middle = " " * (2 * (rows - i))

#         right = "*" * i
#         print(left + middle + right)

# if __name__ == "__main__":
#     Pyramid()

# def V_shape():
#     rows = int(input("enter number of rows: "))
#     for i in range(1, rows + 1):
#         left = "*" * i
#         middle = " " * (2 * (rows - i))
#         right = "*" * i
#         print(left+ middle+right)

# V_shape()


# def Pyramid():
#     rows = int(input("Enter the number of rows: "))
#     for i in range(rows, 0, -1):
#         left = "*" * i
#         middle = " " * (2 * (rows - i))
#         right = "*" * i
#         print(left + middle + right)
#     for i in range(2, rows + 1):
#         left = "*" * i
#         middle = " " * (2 * (rows - i))
#         right = "*" * i
#         print(left+ middle+right)

# Pyramid()

# Write a program that displays the numbers 1 through 10
# using a loop.
# Using while

# n = 1
# while n <= 10:
#     print(n)
#     n += 1


# Using for loop

# for i in range(101):
#     if i % 2 == 0:
#         print(i, end=",")


# for i in range(0, 101, 2):
#     print(i, end="_")

# 39. Write a program that displays even numbers 1 to 50 and
# odd numbers 51 to 100 using a repeating loop.

# for i in range(0, 100):
#     if i <= 50 and i % 2 == 0:
#         print(i, end=",")
#         # i += 1
#     elif i > 50 and i % 2 == 1:
#         print(i, end=",")
    

# for i in range(1,11):
#     for j in range(1,11):
#         product =  i*j
#         print(i, "x", j, "=", product)
#     print("_" * 10)


# for i in range(1, 6):
#     for j in range(1, i+1):
#         print(j, end=" ")
#     print()

# def full_pyramid(rows):
#     for i in range(1, rows + 1):
#         print(" " * (rows - i), end=" ")
#         print("*" * (2 * i - 1))
# full_pyramid(5)



# def inverted_pyramid(rows):
#     for i in range(rows, 0 , -1):
#         print(" " * (rows ))
            # not finished
        