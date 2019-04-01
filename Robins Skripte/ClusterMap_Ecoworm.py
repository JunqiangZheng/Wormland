
# coding: utf-8

# In[192]:


##### IMPORT REQUIRED PACKAGES #####

import matplotlib as plt
from matplotlib import pyplot
from matplotlib import figure
import seaborn as sns; sns.set(color_codes=True)
import pandas as pd
import scipy
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage
import functools


##### PREPARE THE DATA #####

    #Read the file, pandas imports the table as a dataframe
Ecoworm = pd.read_csv("EcoW-data-EVOP.csv", sep = ";")

    #Extract the OTU-columns from the dataframe, using the .iloc parameter
species = Ecoworm.iloc[0:, 8:]

    #when extracting the OTU-columns, the indices (rownames) are gone, we have to manually replace them
    #We can rename the indices to have a clear description of the sample
    #The "axis" parameter tells pandas to concatenate the columns, not the rows
index = pd.concat([Ecoworm['Location'], Ecoworm['Depth'], Ecoworm["Worm"], Ecoworm["No."]], axis = 1)
species.index = index


##### BUILD THE DISTANCEMATRIX #####

    #First we need the distance matrix, this requires so-called linkage values
    #see scipy-cluster manual for more info
speciesLinkage = linkage(species, metric = "braycurtis", method = "weighted")

    #Now we do the actual distance matrix
Dist = scipy.spatial.distance.pdist(species, metric='braycurtis')

    #The matrix is one-dimensional, but we want a redundant square-formatted matrix with
    #the samples in rows as well as columns
    #We then reformat the matrix to a dataframe and again add the indices (rownames and columnnames)
DistRedundant = scipy.spatial.distance.squareform(Dist)
DistRedundantDataFrame = pd.DataFrame(DistRedundant, columns=index, index=index)


##### PREPARE THE VISUALISATIONS #####

    #First we set the parameters for seaborn, so we have sexy visualisations
    #cmap is the colourmap used, here I invert the colours because I think it's nicer
    #we then reduce the fontsize to fit all samplenames into the axis labels
    #seaborn requires a colour-dictionary for the additional row labels, which we get by looping
    #over the indices and assigning a colour per location/worm etc, whichever you like
    #just remember to change the parameters when assigning different factors
cmap = sns.cm.rocket_r
sns.set(font_scale=0.5)
labels = species.index
ColorList = []
for element in labels:
    if "yes" in str(element):
        ColorList.append("#f7c59f")
    elif "no" in str(element):
        ColorList.append("#c7ccdb")
ColorDict = {"Presence" : "#f7c59f", "Absence" : "#c7ccdb"}


##### DO THE CLUSTERMAP #####

    #The input matrix is the redundant dataframe of our distance matrix
    #To avoid doing a distance matrix of our distance matrix again, we assign the linkage we calcu-
    #lated before to our rows and columns. Then we colour the dendrogram leaves with the colour-list
g = sns.clustermap(DistRedundantDataFrame, col_linkage=speciesLinkage, row_linkage=speciesLinkage, 
                   standard_scale=0, square = False, cmap = cmap, row_colors = ColorList, col_colors = ColorList, 
                   linewidths = 0)


    #In this loop we plot the legend to the corresponding leaf-colours and then save our sexy figure
for (label, color) in ColorDict.items():
    g.ax_col_dendrogram.bar(0, 0, color=color,
                            label=label, linewidth=0, width = 40)
g.ax_col_dendrogram.legend(loc="upper right", ncol=1)
g.savefig("Clustermap_Worm.pdf")


##### THE END :) #####

