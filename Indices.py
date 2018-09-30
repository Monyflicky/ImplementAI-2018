
# coding: utf-8

# In[4]:


str_a = "Chicken breasts and thighs, vegetables, prosciutto, tomatoes and herbs make up a dish that's perfect for a shareable dinner."
str1 ="Chicken breasts"
str2 = "vegetables"
str3 = "prosciutto"
str4 = "herbs"

str_b="Cook chicken breasts, skin-side down, in hot butter and oil until browned, about 5 minutes. Flip and cook until they are almost cooked through, about 5 minutes more. Transfer it to a plate." 
str5="chicken breasts"
str6="butter"
str7="oil"
def IndexBegEnd(s1: str, s2:str) -> list:
    n = len(s1)
    m = len(s2)
    if n > m:
        b = s1.find(s2)
        e = b+m+1
        l = [b, e]
        return l
    else:
        return []
print(IndexBegEnd(str_a, str1))
print(IndexBegEnd(str_a, str2))
print(IndexBegEnd(str_a, str3))
print(IndexBegEnd(str_a, str4))
print(IndexBegEnd(str_b, str5))
print(IndexBegEnd(str_b, str6))
print(IndexBegEnd(str_b, str7))

print(IndexBegEnd("About two hours by car north of Tuscany in the Emilia-Romagna region of Italy, is a 2,500-square-kilometre area in the hills of Parma where prosciutto di Parma is made.", str3))
print(IndexBegEnd("By Italian law, it is the only area where prosciutto di Parma is made", str3))
print(IndexBegEnd("As a protected designation of origin, the name prosciutto di Parma is governed by a consortium that allows only hams produced in a specific area, with specific breeds, using specific methods, to be labelled as such.", str3))

    


