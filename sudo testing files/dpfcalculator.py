mother = input("Is mother diebetic    ")
age_diagnosed_mother = int(input("If yes, enter the age diagnosed "))
age_mother = int(input("If no, enter current age "))

father = input("Is father diebetic     ")
age_diagnosed_father = int(input("If yes, enter the age diagnosed "))
age_father = int(input("If no, enter current age "))

grandfather = input("Is father diebetic     ")
age_diagnosed_grandfather = int(input("If yes, enter the age diagnosed "))
age_grandfather = int(input("If no, enter current age "))


grandmother = input("Is father diebetic     ")
age_diagnosed_grandmother = int(input("If yes, enter the age diagnosed "))
age_grnadmother = int(input("If no, enter current age "))


sibling0 = input("Is sibling diebetic    ")
age_diagnosed_sibling0 = int(input("If yes, enter the age diagnosed "))
age_sibling0 =int(input("If no, enter current age "))

sibling1 = input("Is sibling diebetic   ")
age_diagnosed_sibling1 = int(input("If yes, enter the age diagnosed "))
age_sibling1 = int(input("If no, enter current age "))


family = {}
#family = {"mother" : ["No" , 49] , "father" : ["No", 52] , "sibling":{"sibling0" : ["No" , 12] , "sibling1" : ["No",20]}}

family["mother"] = [mother , age_diagnosed_mother , age_mother]
family["father"] = [father , age_diagnosed_father , age_father]
family["grandfather"] = [grandfather , age_diagnosed_grandfather , age_grandfather]
family["grandmother"] = [grandmother , age_diagnosed_grandmother , age_grnadmother]
family["sibling"] = {"sibling0" : [sibling0 , age_diagnosed_sibling0 , age_sibling0] , "sibling1" : [sibling1 , age_diagnosed_sibling1 , age_sibling1]}

yes = []
no = []



for relation in family:
    if relation != "sibling":
        if family[relation][0] == "Yes":
            yes.append((relation , family[relation][1]))
        elif family[relation][0] == "No":
            no.append((relation ,family[relation][2]))
    else:
        for sibling in family[relation]:
            if family[relation][sibling][0] == "Yes":
                yes.append((sibling , family[relation][sibling][1]))
            elif family[relation][sibling][0] == "No":
                no.append((sibling ,family[relation][sibling][2]))



sigma_yes = 0
sigma_no = 0

for data in yes:
    if data[0] == "father" or data[0] == "mother":
        sigma_yes += 0.5*( 88 - data[1])
    #elif data[0] == "grandfather" or data[0] == "grandmother":
    #    sigma_yes += 0.5( 88 - data[1]))
    else:
        sigma_yes += 0.25*(88 - data[1])

for data in no:
    if data[0] == "father" or data[0] == "mother":
        sigma_no += 0.5*(data[1] - 14)
    #elif data[0] == "grandfather" or data[0] == "grandmother":
    #    sigma_yes += 0.5(data[1] - 14))
    else:
        sigma_no += 0.25*(data[1] - 14)

dpf = (sigma_yes + 20)/(sigma_no + 50)

print(dpf)





