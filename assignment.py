import csv
from collections import defaultdict
import gmplot
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import pandas

####################### global data stuctures ######################
crime_type= defaultdict(lambda: 0)
lat_lon=defaultdict(lambda: 0)
ages_to_number_of_victoms={
    "0-18":0,
    "19-30":0,
    "31-50":0,
    "50+":0,
}
####################### global data stuctures end ######################

################################ helpers ###############################
def save_ages(age_affected):
    if age_affected <=18:
        ages_to_number_of_victoms["0-18"]+=1
    elif age_affected <=30:
        ages_to_number_of_victoms["19-30"]+=1
    elif age_affected <=50:
        ages_to_number_of_victoms["31-50"]+=1
    else:    
        ages_to_number_of_victoms["50+"]+=1
########################### helpers  end ###############################

############################## preprocess ##############################
# reads the file and stores the data into an efficciant data structure
def preprocess():
    print("preprocessing...")
    counter=0
    with open('Crime_Data_from_2010_to_Present.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # if counter==10000:
            #     break
            if row["Area Name"]=="West LA":
               
                # somethimes ages may not be reported
                try:
                    age_affected=int(row["Victim Age"].strip())
                    save_ages(age_affected)
                except:
                    continue
                counter+=1
                crime_type[row["Crime Code Description"]]+=1
                # print(row["Date Reported"])
                lat_lon[row["Location "]]+=1
    print("done preprocessing...")
########################## preprocess end ###########################


############################## graph_top_n_crimes ##############################
# graphs the top n crimes in west LA using matplotlib, saves the graph as "top n crimes.png"
def graph_top_n_crimes(top_n, showgraph):
    print("graphing top {} crimes...".format(top_n))
    crimes=[]
    number_of_crimes=[]
    counter=0
    print("\n*****top {} crimes*****".format(top_n))
    # sort the dictionary by keys from greatest to smallest
    for key, value in sorted(crime_type.items(), key=lambda item: (item[1], item[0]),reverse=True):
        if counter==top_n:
            break
        counter+=1
        crimes.append(key.replace(" ","\n"))
        number_of_crimes.append(value)
        print(key,value)
    print("****top {} crimes*****\n".format(top_n))


    y_pos = np.arange(len(crimes))

    plt.figure(1)

    plt.bar(y_pos, number_of_crimes, align='center', alpha=0.5)
    plt.xticks(y_pos, crimes)
    plt.ylabel('number of crimes')
    plt.title('top {} crimes'.format(top_n))
    plt.subplots_adjust(bottom=0.4)
    # plt.subplots_adjust(left=0.05)
    # plt.subplots_adjust(right=0.95)

    plt.savefig('top {} crimes'.format(top_n))
    if showgraph:
        plt.show()
    plt.clf()
    plt.cla()
    plt.close()
############################# graph_top_n_crimes end ############################

############################# graph_age_groups #############################
# uses matplotlib to plot the rang of ages
def graph_age_groups(showgraph):
    print("graphing age groups...")    
    age_groups=[]
    number_of_crimes=[]
    
    # sort the dictionary by keys from greatest to smallest
    for key, value in ages_to_number_of_victoms.items():
        age_groups.append(key.replace(" ","\n"))
        number_of_crimes.append(value)

    y_pos = np.arange(len(age_groups))
    plt.figure(2)

    plt.bar(y_pos, number_of_crimes, align='center', alpha=0.5)
    plt.xticks(y_pos, age_groups)
    plt.ylabel('number of crimes against')
    plt.title('Age groups')

    plt.savefig('crimes against age groups')
    if showgraph:
        plt.show()
    plt.clf()
    plt.cla()
    plt.close()

########################### graph_age_groups end ###########################


############################# plot_maps #############################
# plots colorccoded crome levels(determined by mean median and mode)
# plots seperate html files for top quartile, 50th-75th percentile, 25th to 50th percentile, and bottom quartile
# also plot top n crime sean dependening on top_n
def plot_maps(top_n):
    print("plotting graphs...")    
    # gooogle maps plotters]
    gmap = gmplot.GoogleMapPlotter(34.0412, -118.4426, 14)

    num_crimes=[]

    for key in lat_lon.keys():
        num_crimes.append(lat_lon[key])

    num_crimes_len=len(num_crimes)
    num_crimes.sort(reverse=True)
    addition_factor=int(num_crimes_len/4)
    index=0


    color_array=["#FF0000","#FF6900","#FFD300","#00FF00"]
    color_array_to_crime_level={"#FF0000":"top quartile","#FF6900":"50th-75th percentile","#FFD300":"25th to 50th percentile","#00FF00":"bottom quartile"}


    # plot scatter plot and plot the 4 quartiles
    for color in color_array:
        gmap_temp = gmplot.GoogleMapPlotter(34.0412, -118.4426, 14)
        lat_list=[]
        lon_list=[]

        # fixing an off by one error cause by rounding
        if index+addition_factor>=num_crimes_len:
                addition_factor=num_crimes_len-index-1

        for key in lat_lon.keys():
            
            if lat_lon[key]<=num_crimes[index] and lat_lon[key]>=num_crimes[index+addition_factor]:
                lat_lon_tup=key.replace("(","").replace(")","").split(",")
                try:
                    lat_list.append(float(lat_lon_tup[0]))
                    lon_list.append(float(lat_lon_tup[1]))
                except:
                    continue

        gmap.scatter(lat_list, lon_list, color, size=40, marker=False)
        gmap_temp.scatter(lat_list, lon_list, color, size=40, marker=False)
        gmap_temp.draw("{}({}-{}crimes).html".format(color_array_to_crime_level[color],num_crimes[index+addition_factor],num_crimes[index]))
        index+=addition_factor
    gmap.draw("crime_level_scatter_plot.html")
   

    # plot top n crime areas
    gmap_top_10 = gmplot.GoogleMapPlotter(34.0412, -118.4426, 14)
    lat_list=[]
    lon_list=[]
    for key in lat_lon.keys():
            if lat_lon[key]<=num_crimes[0] and lat_lon[key]>=num_crimes[top_n-1]:
                lat_lon_tup=key.replace("(","").replace(")","").split(",")
                try:
                    lat_list.append(float(lat_lon_tup[0]))
                    lon_list.append(float(lat_lon_tup[1]))
                except:
                    continue
    gmap_top_10.scatter(lat_list, lon_list, "#FF0000", size=40, marker=False)
    gmap_top_10.draw("top-{}.html".format(top_n))
############################# plot_maps end #############################
        


if __name__ == "__main__":
    # preprocess the data and store it in efficcant data strucctures
    preprocess()

    # plot the maps using google maps API, and also plot the top 20
    plot_maps(top_n=20)

    # graph the number of crimes for the stipulated age groups
    # toggle showgraph to see graph using the matplotlib interfacce(so that y0ou can adjust the dimentions)
    graph_age_groups(showgraph=False)

    # graph the top 3 crimes
    # toggle showgraph to see graph using the matplotlib interfacce(so that y0ou can adjust the dimentions)
    graph_top_n_crimes(top_n=3,showgraph=False)
