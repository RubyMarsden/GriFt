
# finding the smallest 'number of sources' with change of 0.1%
def test_precision(total_Ft, total_Ft_1, total_Ft_2, total_Ft_3):
    print(total_Ft, ", ", total_Ft_1, ", ", total_Ft_2, ", ", total_Ft_3)
    if total_Ft_1 and total_Ft_2 and total_Ft_3 is not None:
        print(total_Ft_2, total_Ft_1)
        if abs((total_Ft - total_Ft_1)/ total_Ft) < 0.001 and abs((total_Ft_1 - total_Ft_2)/ total_Ft_1) < 0.001 and\
                abs((total_Ft_2 - total_Ft_3)/total_Ft_2) < 0.001:
            return True
    else:
        return False


total_Ft_cache = {}
total_Ft_cache[0] = None
total_Ft_cache[1] = None
total_Ft_cache[2] = None
total_Ft_cache[3] = None
number_of_sources = 10000
sources = generate_sources(shape, number_of_sources)
n=3
while test_precision(total_Ft_cache[n], total_Ft_cache[n-1], total_Ft_cache[n-2], total_Ft_cache[n-3]) is False:
    number_of_sources += 10000
    sources = generate_sources(shape, number_of_sources)
    total_Ft = sample_total_Ft(shape, sources, shape.max_z)
    total_Ft_cache[n+1] = total_Ft
    n += 1

print(total_Ft_cache[n], total_Ft_cache[n-1], total_Ft_cache[n-2], total_Ft_cache[n-3], len(sources))
