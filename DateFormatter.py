

months = ["Januar", "Februar", "Marts", "April", "Maj" , "Juni", "Juli", "August", "September", "Oktober", "November", "December"]
length = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
searches = []
for i, month in enumerate(months):
    for j in range(length[i]):
        searches.append(f"https://da.wikipedia.org/wiki/{j+1}._{month}")
        
print(searches)