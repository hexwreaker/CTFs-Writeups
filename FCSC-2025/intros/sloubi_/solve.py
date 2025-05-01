

s = "4B}mCuCNJmeVhvCzQusFHS7{2gCBCrQW"

for i in range(32):
    print(s[(17 * i + 51) % 32], end='')
