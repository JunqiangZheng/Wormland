setwd('C:/Users/deisy/Desktop/PhD/05_Courses_Evop/Wormland/Wormland/')

files = system('ls *Network.csv', intern = T)

# files = list.files(pattern="*Network.csv")

for ( i in 1:length(files)){
  name = gsub(pattern = '_Network.csv', 
              replacement = '',
              x = files[i])
  ### Filter the data in the loop
  x = read.csv(files[i])
  x = x[,c(1:3,5)]
  x$wTO_sign = ifelse(x$pval_sig< 0.05, x$wTO_sign, 0)
  assign(name, x)
}

require(wTO)
NetVis(Node.1 = USA10n$Node.1, Node.2 = USA10n$Node.2,
       wTO = USA10n$wTO_sign, pval = USA10n$pval_sig, 
       MakeGroups = 'louvain', cutoff = list(kind = "Threshold", value = 0.1))


require(igraph)
g <- graph_from_data_frame(USA10n)

