def Part():
    rows = int(input("Enter the number of rows: "))
    for i in range(0, rows + 1):
        print("*" * i, "\n")

if __name__ == "__main__":
    Part()