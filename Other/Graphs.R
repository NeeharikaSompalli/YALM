library(plotly)

d<-read.csv("/Users/darshak/Documents/Projects/YALM/uniformResults.csv")
matplot(d$Hot....Almost., cbind(d$tier1.time, d$tier2.time, d$Sum), pch=c(0,1), col = c("Red", "Blue", "Green"), main="Hot % vs Time", ylab = "Values", xlab = "Hot %", type = "l", lw = c(1,0.75), lt = c(1,1,1))
legend("topright", lty = c(1, 1), col = c("Red", "Blue", "Green"), legend = c("Cold Time", "Hot time" , "Total Time"), box.lwd = 0, inset=c(-0.2,0))



d2<-read.csv("/Users/darshak/Documents/Projects/YALM/randomSize.csv")
matplot(d2$Hot....Almost., cbind(d2$Tier.1..time.size., d2$Tier.2..time.size., d2$Sum), pch=c(0,1), col = c("Red", "Blue", "Green"), main="Hot % vs Time", ylab = "Values", xlab = "Hot %", type = "l", lw = c(1,0.75), lt = c(1,1,1))
legend("topright", lty = c(1, 1), col = c("Red", "Blue", "Green"), legend = c("Cold Time", "Hot time" , "Total Time"), box.lwd = 0, inset=c(-0.2,0))

plot1<-plot_ly(x = d2$Hot....Almost., y = d2$Total.Cost, name = "Total Cost",type = "scatter", mode = c("markers", "lines"))%>% add_trace(y = d2$Hot.Cost, name = "Hot Cost", mode = 'lines+markers') %>%
  add_trace(y = d2$Cold.Cost, name = "Cold Cost", mode = 'lines+markers') %>% layout(title = "Total Cost vs Hot % (Random Size Objs)", xaxis = list(title = 'Hot %'), yaxis = list(title = 'Total Cost'))

plot2<-plot_ly(x = d$Hot....Almost., y = d$tier1.time, name = "Cold Time",type = "scatter", mode = c("markers", "lines"))%>% add_trace(y = d$tier2.time, name = "Hot Time", mode = 'lines+markers') %>%
  add_trace(y = d$Sum, name = "Total Time", mode = 'lines+markers') %>% layout(title = "Time vs Hot % (Uniform Size Objs)", xaxis = list(title = 'Hot %'), yaxis = list(title = 'Access Time'))

plot3<-plot_ly(x = d2$Hot....Almost., y = d2$Tier.1..time.size., name = "Cold Time",type = "scatter", mode = c("markers", "lines"))%>% add_trace(y = d2$Tier.2..time.size., name = "Hot Time", mode = 'lines+markers') %>%
  add_trace(y = d2$Sum, name = "Total Time", mode = 'lines+markers') %>% layout(title = "Time vs Hot % (Random Size Objs)", xaxis = list(title = 'Hot %'), yaxis = list(title = 'Access Time'))

plot4<-plot_ly(x = d2$Total.Cost, y = d2$Tier.1..time.size., name = "Cold Time",type = "scatter", mode = c("markers", "lines"))%>% add_trace(y = d2$Tier.2..time.size., name = "Hot Time", mode = 'lines+markers') %>%
  add_trace(y = d2$Sum, name = "Total Time", mode = 'lines+markers') %>% layout(title = "Time vs Total Cost (Random Size Objs)", xaxis = list(title = 'Total Cost'), yaxis = list(title = 'Access Time'))

d = read.csv("/Users/darshak/Documents/Projects/YALM/powerlaw15.csv", header=FALSE)
hist(d$V1, breaks = 1000, main = "A = 15")


d = read.csv("/Users/darshak/Documents/Projects/YALM/powerlaw10.csv", header=FALSE)
hist(d$V1, breaks = 1000, main = "A = 10")

d = read.csv("/Users/darshak/Documents/Projects/YALM/powerlaw5.csv", header=FALSE)
hist(d$V1, breaks = 1000, main = "A = 5")

d = read.csv("/Users/darshak/Documents/Projects/YALM/powerlaw1.csv", header=FALSE)
hist(d$V1, breaks = 1000, main = "A = 1")



d3 <- read.csv("/Users/darshak/Documents/Projects/YALM/randomSize\ Powerlaw.csv")

plot3<-plot_ly(x = d3$Hot....Almost., y = d3$Tier.1..time.size., name = "Cold Time",type = "scatter", mode = c("markers", "lines"))%>% add_trace(y = d3$Tier.2..time.size., name = "Hot Time", mode = 'lines+markers') %>%
  add_trace(y = d3$Sum..time., name = "Total Time", mode = 'lines+markers') %>% layout(title = "Time vs Hot % (Random Size Objs - PowerLaw)", xaxis = list(title = 'Hot %'), yaxis = list(title = 'Access Time'))


plot5<-plot_ly(x = d$hot.p, y = d$Hot_time/d$Hot_accessed_size, name = "Hot Time",type = "scatter", mode = c("markers", "lines"))%>% add_trace(y = d$Cold_time/d$Cold_accessed_size, name = "Cold Time", mode = 'lines+markers') %>%layout(title = "Time vs Hot % (Random Size Objs)", xaxis = list(title = 'Hot %'), yaxis = list(title = 'Access Time'))

plot9<-plot_ly(x = d3$hot.p, y = d3$Hot_time, name = "Hot Time",type = "scatter", mode = c("markers", "lines"))%>% add_trace(y = d3$Cold_time, name = "Cold Time", mode = 'lines+markers') %>%layout(title = "Time vs Hot % (Random Size Objs)", xaxis = list(title = 'Hot %'), yaxis = list(title = 'Access Time'))
plot9
plot10<-plot_ly(x = d3$hot.p, y = d3$Hot_time + d3$Cold_time, name = "Hot Time",type = "scatter", mode = c("markers", "lines"))%
plot10<-plot_ly(x = d3$hot.p, y = d3$Hot_time + d3$Cold_time, name = "Hot Time",type = "scatter", mode = c("markers", "lines"))
plot10

plot10<-plot_ly(x = hp, y = tp, name = "Hot Time",type = "scatter", mode = c("markers", "lines"))%>%layout(title = "Time vs Hot % (Random Size Objs - PowerLaw w Mean Policy)", xaxis = list(title = 'Hot %'), yaxis = list(title = 'Access Time'))


