from sklearn.linear_model import LinearRegression , LogisticRegression
from model import *
# importing Flask and other modules
from flask import Flask, redirect, request, render_template,url_for

# Flask constructor
app = Flask(__name__)


#global variable for sibling
#sibling = 2

# A decorator used to tell the application
# which URL is associated function

def load_data_from_dataset_for_female():

    evidence=[]
    labels=[]
    with open("dataset.csv") as file:
        reader=csv.reader(file)
        next(reader)
        for row in reader:
            #0 for yes and 1 for no
            evidence.append([
                            int(row[0]),
                            int(row[1]),
                            int(row[2]),
                            int(row[3]),
                            float(row[4]),
                            float(row[5]),
                            float(row[6]),
                            int(row[7]),
                            ])
            labels.append(int(row[8]))
    
    return (evidence , labels)

def load_data_from_dataset_for_male():

    evidence=[]
    labels=[]
    with open("dataset.csv") as file:
        reader=csv.reader(file)
        next(reader)
        for row in reader:
            #0 for yes and 1 for no
            evidence.append([
                            int(row[1]),
                            int(row[2]),
                            int(row[3]),
                            float(row[4]),
                            float(row[5]),
                            float(row[6]),
                            int(row[7]),
                            ])
            labels.append(int(row[8]))
    
    return (evidence , labels)

countries = []
with open("countries.csv") as country_file:
    reader=csv.reader(country_file)
    for row in reader:
        countries.append(row[0])


@app.route('/' , methods = ["GET"])
def index():
    return render_template("website.html")

@app.route('/form', methods =["GET", "POST"])
def data():
    if request.method == "POST":

        name_input = request.form.get("name_input")
        sex_input = request.form.get("sex_input")
        pregnancy_input = request.form.get("pregnancy_input")
        glucose_input = request.form.get("glucose_input")
        bp_input = request.form.get("bp_input")
        skin_input = request.form.get("skin_input")
        insulin_input = request.form.get("insulin_input")
        bmi_input = request.form.get("bmi_input")
        dbf_input = request.form.get("dbf_input")
        age_input = request.form.get("age_input")

        

        if sex_input == "Female":
            if not pregnancy_input:
                return render_template("error.html" , pregnancy = "Pregnancy")
            evidence , labels = load_data_from_dataset_for_female()
            pregnancy , glucose,bp,skinthickness,insulin,bmi,dpf,age = pregnancy_input , glucose_input,bp_input,skin_input,insulin_input,bmi_input,dbf_input,age_input
            d = {
                'Pregnancy' : float(pregnancy) ,
                'Glucose' : float(glucose),
                'Bp' : float(bp),
                'Skin Thickness' : float(skinthickness),
                'Insulin' : float(insulin),
                'BMI' : float(bmi),
                'DPF' : float(dpf),
                'AGE' : float(age),
            }
            df = pd.DataFrame([d])
            df.to_csv("user_data.csv")

            testing_data = pd.read_csv("user_data.csv",index_col=False)
            testing_features = ["Pregnancy","Glucose","Bp","Skin Thickness","Insulin","BMI","DPF","AGE"]
            test = testing_data[testing_features]

            model = RandomForestRegressor(random_state=1)
            #model = LinearRegression()
            model.fit(evidence , labels)
            prediction = model.predict(test)
            print (model.predict(test))
            probability = float(prediction[0]*100)

        elif sex_input == "Male":
            evidence , labels = load_data_from_dataset_for_male()
            glucose,bp,skinthickness,insulin,bmi,dpf,age =  glucose_input,bp_input,skin_input,insulin_input,bmi_input,dbf_input,age_input
            d = {
                'Glucose' : float(glucose),
                'Bp' : float(bp),
                'Skin Thickness' : float(skinthickness),
                'Insulin' : float(insulin),
                'BMI' : float(bmi),
                'DPF' : float(dpf),
                'AGE' : float(age),
            }
            df = pd.DataFrame([d])
            df.to_csv("user_data.csv")

            testing_data = pd.read_csv("user_data.csv",index_col=False)
            testing_features = ["Glucose","Bp","Skin Thickness","Insulin","BMI","DPF","AGE"]
            test = testing_data[testing_features]

            model = RandomForestRegressor(random_state=1)
            #model = LinearRegression()
            model.fit(evidence , labels)
            prediction = model.predict(test)
            print (model.predict(test))
            probability = float(prediction[0]*100)
        
        model_prob = probability

        
        #contribution of locatation in probability
        
        probability += color_weight[user_location_color]
        
        return render_template("result.html",result = float(probability),result_brand = int(probability),location_weight = float(color_weight[user_location_color]),model_prob = float(model_prob), name = name_input , country = country,sex = sex_input)

        
    return render_template("form.html")

@app.route('/model', methods =["GET"])
def model():
    return render_template("model.html")

@app.route('/familyhistory' , methods = ["GET" , "POST"])
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
            if data[0] == "grandfather" or data[0] == "grandmother":
               sigma_yes += 0.25*( 88 - data[1])
            else:
                sigma_yes += 0.5*(88 - data[1])

        for data in no:
            if data[0] == "grandfather" or data[0] == "grandmother":
                sigma_no += 0.25*(data[1] - 14)
            else:
                sigma_no += 0.5*(data[1] - 14)

        global dpf
        dpf = (sigma_yes + 20)/(sigma_no + 50)

        return render_template('dpfresult.html' , dpf = round(dpf,3))
    else:
        return render_template("dpfcalculator.html" , siblings = no_of_siblings)
    
    

@app.route('/sibling' , methods = ["GET" , "POST"])
def sibling():
    global no_of_siblings
    if request.method == "POST":
        no_of_siblings = int(request.form.get("no_of_siblings"))
        return redirect(url_for('familyhistory'))
    else:
        return render_template('sibling_input.html')

@app.route('/location',methods=["GET","POST"])
def location():
    if request.method == "POST":
        global country
        global user_location_color
        country = request.form.get('country')
        global color_weight
        categories = {}
        color_weight = {}
        categories['red'] = ['Russia','India','Pakistan','China','United States of America','Indonesia']
        categories['orange'] = ['Brazil','Egypt','Italy','Germany','United Kingdom','Iran','Turkey','Japan','Bangladesh','Vietnam','Philippines','Malta']
        categories['yellow'] = ['Canada','Mexico','Colombia','Venezuela','Chile','Peru','Argentina','South Africa','Angola','Democratic Republic of the Congo',
                                'Uganda','Tanzania','Kenya','Sudan','Ethiopia','Ghana','Nigeria','Algeria','Morocco','Yemen','Saudi Arabia',
                                'Iraq','Syria','Spain','Portugal','France','Belgium','Netherlands','Greece','Romania','Ukraine','Sweden','Kazakhstan',
                                'Uzbekistan','Afghanistan','Nepal','Sri Lanka','Malaysia','Myanmar (formerly Burma)','Australia','North Korea','South Korea','Andorra',
                                'Cabo Verde','Cyprus','Czechia (Czech Republic)','Holy See','Hungary','Lebanon','Singapore','Switzerland','Liechtenstein',
                                'Luxembourg','Monaco','Poland']
        categories['green'] = ['Antigua and Barbuda','Bahamas','Barbados','Cuba','Dominica','Dominican Republic','Grenada','Haiti','Jamaica','Saint Kitts and Nevis',
                                'Saint Lucia','Saint Vincent and the Grenadines','Trinidad and Tobago','Ecuador','Bolivia',"CÃ´te d'Ivoire'",'Burkina Faso',
                                'Libya','Senegal','Gambia','Zambia','Zimbabwe','Malawi','Mozambique','Madagascar','Somalia','Jordan','United Arab Emirates',
                                'Azerbaijan','Bulgaria','Belarus','Norway','Ireland','Tajikistan','Cambodia','Papua New Guinea','Austria','Brunei',
                                'Cameroon','Comoros','Finland','Israel','Thailand','Mali','Mauritius','Niger']
        categories['purple'] = ['Denmark','Marshall Islands',]
        categories['dark blue'] = ['Iceland','Guyana','Suriname','Guinea-Bissau','Equatorial Guinea','Djibouti','Eswatini (fmr. "Swaziland")','Bhutan','Bosnia and Herzegovina','']
        categories['light blue'] = ['Uruguay','Paraguay','Namibia','Botswana','Rwanda','Burundi','Eritrea','Oman','Qatar','Kuwait','Liberia','Sierra Leone',
                                    'Guinea','Gabon','Congo (Congo-Brazzaville)','Central African Republic','Chad','South Sudan','Lesotho','Estonia',
                                    'Latvia','Lithuania','Georgia','Turkmenistan','Kyrgyzstan','Mongolia','Laos','Fiji','New Zealand','Albania','Armenia','Bahrain',
                                    'Belize','Benin','Costa Rica','Croatia','El Salvador','Guatemala','Kiribati','Maldives','Mauritania','Moldova']


        for color in categories:
            if country in categories[color]:
                user_location_color = color

        color_weight['red'] = 1.177
        color_weight['orange'] = 0.132
        color_weight['yellow'] = 0.065
        color_weight['green'] = 0.013
        color_weight['light blue'] = 0.006
        color_weight['dark blue'] = 0.001
        color_weight['purple'] = 0
        
                
        return redirect(url_for('data'))
    else:
        return render_template('location.html' , countries = countries)

if __name__=='__main__':
    app.run()
