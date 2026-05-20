string="salman khan and imrankhan "
l=[]
new_str=""
for i in string:
    if i in l:
        pass
    else:
        l.append(i)
        new_str=new_str+i


print(new_str)
