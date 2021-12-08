def contains(arr1, arr2):
    # Check array lengths
    n = len(arr2)
    m = len(arr1)
    # Compare each value
    for i in range(n):
        for j in range(m):
            if arr2[i] == arr1[j]:
                return 1
    return 0
