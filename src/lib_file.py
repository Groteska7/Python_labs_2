def line_line(row: str, ln: int, dot="="):
    if len(row)>ln:
        raise ValueError("Строка длиннее конечной длинны")
    else:
        ln=ln-len(row)
        if ln%2!=0:
            return dot*(ln//2+1)+row+dot*(ln//2)
        else:
            return dot*(ln//2)+row+dot*(ln//2)