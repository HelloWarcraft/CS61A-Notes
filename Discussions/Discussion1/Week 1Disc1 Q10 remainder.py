def unique_digits(n):
    """Return the number of unique digits in positive integer n

    >>> unique_digits(8675309) # All are unique
    7
    >>> unique_digits(1313131) # 1 and 3
    2
    >>> unique_digits(13173131) # 1, 3, and 7
    3
    >>> unique_digits(10000) # 0 and 1
    2
    >>> unique_digits(101) # 0 and 1
    2
    >>> unique_digits(10) # 0 and 1
    2
    """
    temp=n
    remainder=0
    while temp!=0:
        remainder=temp%10
        temp=temp//10
        # 依次取出所有的remainder，结果例如131的第一个和第三个remainder一直，只统计一次，这个和解？

