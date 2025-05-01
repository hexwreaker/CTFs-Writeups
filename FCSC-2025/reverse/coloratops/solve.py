

# key = hash(user_input)
iv = 0


suite = [0, 0, 0, 0, 0, 9, 6, 3, 6, 7, 6, 5, 7, 4, 6, 2, 7, 7, 2, 9, 6, 7, 7, 5, 1, 6, 2, 8, 4, 3, 6, 8, 5, 4, 9, 2, 9, 1, 2, 7, 1, 1, 4, 4, 2, 5, 4, 8, 6, 1, 6, 7, 4, 9, 1, 9, 5, 4, 3, 9, 9, 9, 3]
suite = suite[5:]
suite_str = [str(i) for i in suite]
print(''.join(suite_str))
tab = [0x0FFFFFFFF, 0x802D2FFF, 0x0FF595EFF, 0x0FF924CFF, 0x0FFAE43FF, 0x0FFCA3AFF, 0x8AC926FF, 0x52A675FF, 0x6A4C93FF, 0x1982C4FF]


# print(''.join(suite))
#0000096367657462772967751628436854929127114425486167491954399930
#FCSC{9636765746277296775162843685492912711442548616749195439993}

hex_suite = '0123456789abcdef'

suites = [b'a']*16
suites[0] = b'\t\x02\x07\x06\x04\x07\x06\t\x06\x06\x01\x08\x03\x04\x07\x06\x02\x08\x02\t\x03\x03\x08\x06\x01\x06\x07\x07\x03\t\x01\x06\t\x08\x05\x08\x02\x07\x05\x07\t\x03\x07\x02\x08\x03\x04\x06\x01\x03\x01\x02\x05\x06\x08\x05\x01\x02'
suites[1] = b'\x08\x02\x02\x01\x07\x02\x02\x08\x08\x01\x04\t\x08\x02\x05\x01\x03\x06\x01\x05\x06\t\x03\x04\x04\x07\x07\x08\x07\x04\x03\x04\x07\x08\x04\x01\x03\x08\x04\x08\x03\x08\x02\x05\x07\x03\t\x08\x05\x06\x06\x07\x01\x02\x03\x05\x04\x06'

for j in range(16):
    print(''.join([str(i) for i in suites[j]]))



# diff_suite = [suite[i] - a_suite[i] for i in range(len(a_suite))]
# print(diff_suite)
# # print(len(diff_suite))
# hex_pos_suite = [(10+diff_suite[i])%16 for i in range(len(diff_suite))]
# print(hex_pos_suite)
# final_suite = ''.join([hex_suite[hex_pos_suite[i]] for i in range(len(hex_pos_suite))])
# print(final_suite)

# a_suite = ''.join([hex_suite[(9+i)%16] for i in a_suite])
# print(a_suite)

# FCSC{294af9ae8c5cc6eaead5b7095bca8b31ab979c9665ea69ac09cea9ec17}
# FCSC{1001101001011011102222222222222222222222223332222222222233}



# 1 -> bordeaux
# 2 -> rouge
# 3 -> orange
# 4 -> orange clair
# 5 -> jaune
# 6 -> vert clair
# 7 -> vert sapin
# 8 -> mauve
# 9 -> bleu

#96367657462772967751628436854929127114425486167491954399930
#                                                        0d}
#FCSC{393005dd2218ba02bfda28559813de7586c267140d08e1e83a4ae5a61d}
#                                                        2d}
#                                                        9d}
#                                                        bd}
