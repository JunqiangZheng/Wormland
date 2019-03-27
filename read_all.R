setwd('C:/Users/deisy/Desktop/PhD/05_Courses_Evop/Wormland/Wormland/')

files = system('ls *Network.csv', intern = T)

for ( i in 1:length(files)){
  name = gsub(pattern = '_Network.csv', 
              replacement = '',
              x = files[i])
  assign(name, read.csv(files[i]))
}