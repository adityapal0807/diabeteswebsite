def familyhistory():
    if request.method == "POST":
        parent_m = request.form.get("parent_m")
        parent_f = request.form.get("parent_f")
        age_diagnosed_m = int(request.form.get("age_diagnosed_m"))
        age_diagnosed_f = int(request.form.get("age_diagnosed_f"))
        age_m = int(request.form.get("age_m"))
        age_f = int(request.form.get("age_f"))
        grandmother = request.form.get("grandmother")
        grandfather = request.form.get("grandfather")
        age_diagnosed_gm = int(request.form.get("age_diagnosed_gm"))
        age_diagnosed_gf = int(request.form.get("age_diagnosed_gf"))
        age_gm = int(request.form.get("age_gm"))
        age_gf = int(request.form.get("age_gf"))
        

        family = {}

        family["mother"] = [ parent_m , age_diagnosed_m , age_m]
        family["father"] = [ parent_f , age_diagnosed_f , age_f]
        family["grandfather"] = [grandfather , age_diagnosed_gf , age_gf]
        family["grandmother"] = [grandmother , age_diagnosed_gm , age_gm]
        family["sibling"] = {}

        

        for sibling_no in range(0,no_of_siblings):
            sib = 'sibling'
            age_diagnosed_s = 'age_diagnosed_s'
            age_s = 'age_s'
            s = sib + str(sibling_no)
            s_answer = s + 'answer'
            s_age_diagnosed = age_diagnosed_s + str(sibling_no) 
            s_age = age_s + str(sibling_no)
            s_answer = request.form.get("{}".format(s_answer))
            s_age_diagnosed= int(request.form.get("{}".format(s_age_diagnosed)))
            s_age = int(request.form.get("{}".format(s_age)))

            family["sibling"][s] = [s_answer , s_age_diagnosed , s_age]
            
            

        #main calculation

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
            elif data[0] == "grandfather" or data[0] == "grandmother":
               sigma_yes += 0.5*( 88 - data[1])
            else:
                sigma_yes += 0.25*(88 - data[1])

        for data in no:
            if data[0] == "father" or data[0] == "mother":
                sigma_no += 0.5*(data[1] - 14)
            #elif data[0] == "grandfather" or data[0] == "grandmother":
            #    sigma_yes += 0.5(data[1] - 14))
            else:
                sigma_no += 0.25*(data[1] - 14)

        global dpf
        dpf = (sigma_yes + 20)/(sigma_no + 50)

        return render_template('dpfresult.html' , dpf = round(dpf,3))
    else:
        return render_template("dpfcalculator.html" , siblings = no_of_siblings)
    