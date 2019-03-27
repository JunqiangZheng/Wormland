setwd('C:/Users/deisy/Desktop/PhD/05_Courses_Evop/Wormland/Wormland/')

files = system('ls *Network.csv', intern = T)

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
