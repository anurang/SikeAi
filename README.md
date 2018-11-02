# SikeAI


## prerequisits
have the file 
Crime_Data_from_2010_to_Present.csv that uses the excel format!
## python modules used
* csv
* collections  
* gmplot
* matplotlib
* numpy 
* pandas

# Usage
```
python assignment.py
```

# Results!
## Scatter plot!
My program enables you to plot the crime number of crimes on a map and color codes them according to the top quartile, 50th-75th percentile, 25th to 50th percentile, and bottom quartile
![Alt text](/images/scatter_plot.png?raw=true "Optional Title")

* Red: top 25% 17-1163 crimes!
* Orange: top 50% to top 75%: 7-17 crimes!
* Yellow bottom 25% to bottom 50%: 2-7 crimes!
* Green: bottom 25%: 1-2 crimes!

*Notice this data is skewed to the right! This means that areas prone to crimes have an extreme amount of crime and areas not prone to crime have very little crime! Very interesting…*

## Plotting the worst 20 (Unexpected results!):
My program also lets you plot the worst crime areas allowing you to have a deeper understanding of the data….
![Alt text](/images/top_20.png?raw=true "Optional Title")


Plotting top 20 gave very interesting results, contrary to popular belief, **2 spots in Westwood fall under the top 5 crime areas, in-fact Westwood is in the top 10!**

![Alt text](/images/westwood.png?raw=true "Optional Title")

### Worst 5
Unsurprisingly, the top 5 worst places were the popular malls and outlet areas, which include century city, westside bulaward and Wilshire bulaward

Surprisingly though WESTWOOD was in the top 5!
![Alt text](/images/top_5.png?raw=true "Optional Title")


### The worst!
The number one spot for crime was century city
![Alt text](/images/century_city.png?raw=true "Optional Title")

## graphing the Most common types of crimes
The top n types of crime can be attained by using the function
```
graph_top_n_crimes(top_n, showgraph)
```
graph_top_n_crimes:
* outputs top n crimes along with the number in the consul
* Plots a graph that is saved as “top n crimes.png”
* if you want to look at the graph using matplotlib, toggle the showgraph arguement
![Alt text](/images/top_3_crimes.png?raw=true "Optional Title")

## Plotting crimes against age groups:
Plots the crimes affecting specific age group ranges. Works a lot like graph_top_n_crimes
```
graph_age_groups(showgraph)
```
![Alt text](/images/crimes_against_age_groups.png?raw=true "Optional Title")
