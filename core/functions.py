def arr_in_html(arr):
    # s = ""
    s = "<table cellpadding=\"5\" border='1' style='border-collapse: collapse;'>\n"
    for row in arr:
        s += "\t<tr>\n"
        for col in row:
            s += "\t\t<td>"
            s += str(col)
            s += "</td>\n"
        s += "\t</tr>\n"

    s += "</table>"
    # cur.close()
    # db.close()
    return s
