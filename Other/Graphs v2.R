library(plotly)


#strptime(d[2,4], "%Y-%m-%d %H:%M:%OS")

bucketMetrics <- read.csv('/Users/darshak/Documents/Projects/YALM/bucketMetrics_2018-04-21\ 165850.273438_Basic_policy.csv')



ay <- list(
  tickfont = list(color = "red"),
  overlaying = "y",
  side = "right",
  title = "No of Objs in Tier"
)

basic_plot <- plot_ly(x = c(1:16), y = (bucketMetrics$time_size), name = "Time",type = "scatter", mode = c("markers", "lines")) %>% 
  add_trace(y = (bucketMetrics$Cold_Objs_a), name = "Cold Objs", mode = 'lines+markers', yaxis = "y2", color = list('red')) %>% 
  add_trace(y = (bucketMetrics$Hot_Objs_a), name = "Hot Objs", mode = 'lines+markers', yaxis = "y2", color = list('red')) %>% 
  layout(title = "Basic Policy", xaxis = list(title = 'Time Points'), yaxis = list(title = 'Access Time (s)'), yaxis2 = ay)
basic_plot

c_h_bucketMetrics <- read.csv('/Users/darshak/Documents/Projects/YALM/bucketMetrics_2018-04-22\ 122719-892813_C_t_H.csv')


### NEW VS BASIC ####

c_h_plot <- plot_ly(x = c(1:14), y = (c_h_bucketMetrics$time_size), name = "Time NP",type = "scatter", mode = c("markers", "lines")) %>% 
  add_trace(y = (c_h_bucketMetrics$Cold_Objs_a), name = "Cold Objs NP", mode = 'lines+markers', yaxis = "y2", color = list('red')) %>% 
  add_trace(y = (c_h_bucketMetrics$Hot_Objs_a), name = "Hot Objs NP", mode = 'lines+markers', yaxis = "y2", color = list('red')) %>% 
  add_trace(y = (bucketMetrics$time_size[1:14]), name = "Time BP", mode = 'lines+markers', yaxis = "y1", color = list('red')) %>%
  add_trace(y = (bucketMetrics$Cold_Objs_a[1:14]), name = "Cold Objs BP", mode = 'lines+markers', yaxis = "y2", color = list('red')) %>% 
  add_trace(y = (bucketMetrics$Hot_Objs_a[1:14]), name = "Hot Objs BP", mode = 'lines+markers', yaxis = "y2", color = list('red')) %>% 
  layout(title = "Cold To Hot (LRU)", xaxis = list(title = 'Time Points'), yaxis = list(title = 'Access Time (s)'), yaxis2 = ay)
c_h_plot

#######

### DELTA VS NEW ####

d_c_h_bucketMetrics <- read.csv('/Users/darshak/Documents/Projects/YALM/bucketMetrics_2018-04-22\ 145921-124021_D_C_t_H.csv')


d_c_h_plot <- plot_ly(x = c(1:14), y = (c_h_bucketMetrics$time_size), name = "Time LRUP",type = "scatter", mode = c("markers", "lines")) %>% 
  add_trace(y = (c_h_bucketMetrics$Cold_Objs_b), name = "Cold Objs LRUP", mode = 'lines+markers', yaxis = "y2", color = list('red')) %>% 
  add_trace(y = (c_h_bucketMetrics$Hot_Objs_b), name = "Hot Objs LRUP", mode = 'lines+markers', yaxis = "y2", color = list('red')) %>% 
  add_trace(y = (bucketMetrics$time_size[1:14]), name = "Time BP", mode = 'lines+markers', yaxis = "y1", color = list('red')) %>%
  add_trace(y = (bucketMetrics$Cold_Objs_b[1:14]), name = "Cold Objs BP", mode = 'lines+markers', yaxis = "y2", color = list('red')) %>% 
  add_trace(y = (bucketMetrics$Hot_Objs_b[1:14]), name = "Hot Objs BP", mode = 'lines+markers', yaxis = "y2", color = list('red')) %>% #### DELTA FROM NOW
  add_trace(y = (d_c_h_bucketMetrics$time_size[1:14]), name = "Time DP", mode = 'lines+markers', yaxis = "y1", color = list('red')) %>%
  add_trace(y = (d_c_h_bucketMetrics$Cold_Objs_b[1:14]), name = "Cold Objs DP", mode = 'lines+markers', yaxis = "y2", color = list('red')) %>% 
  add_trace(y = (d_c_h_bucketMetrics$Hot_Objs_b[1:14]), name = "Hot Objs DP", mode = 'lines+markers', yaxis = "y2", color = list('red')) %>% 
  layout(title = "Cold To Hot (Delta)", xaxis = list(title = 'Time Points'), yaxis = list(title = 'Access Time (s)'), yaxis2 = ay)
d_c_h_plot





d_c_h_plot2 <- plot_ly(x = c(1:14), y = (c_h_bucketMetrics$time_size), name = "Time LRUP",type = "scatter", mode = c("markers", "lines")) %>% 
  add_trace(y = (c_h_bucketMetrics$Cold_Size_b), name = "Cold Objs LRUP", mode = 'lines+markers', yaxis = "y2", color = list('red')) %>% 
  add_trace(y = (c_h_bucketMetrics$Hot_Size_b), name = "Hot Objs LRUP", mode = 'lines+markers', yaxis = "y2", color = list('red')) %>% 
  add_trace(y = (bucketMetrics$time_size[1:14]), name = "Time BP", mode = 'lines+markers', yaxis = "y1", color = list('red')) %>%
  add_trace(y = (bucketMetrics$Cold_Size_b[1:14]), name = "Cold Objs BP", mode = 'lines+markers', yaxis = "y2", color = list('red')) %>% 
  add_trace(y = (bucketMetrics$Hot_Size_b[1:14]), name = "Hot Objs BP", mode = 'lines+markers', yaxis = "y2", color = list('red')) %>% #### DELTA FROM NOW
  add_trace(y = (d_c_h_bucketMetrics$time_size[1:14]), name = "Time DP", mode = 'lines+markers', yaxis = "y1", color = list('red')) %>%
  add_trace(y = (d_c_h_bucketMetrics$Cold_Size_b[1:14]), name = "Cold Objs DP", mode = 'lines+markers', yaxis = "y2", color = list('red')) %>% 
  add_trace(y = (d_c_h_bucketMetrics$Hot_Size_b[1:14]), name = "Hot Objs DP", mode = 'lines+markers', yaxis = "y2", color = list('red')) %>% 
  layout(title = "Cold To Hot (Delta)", xaxis = list(title = 'Time Points'), yaxis = list(title = 'Access Time (s)'), yaxis2 = ay)
d_c_h_plot2


hot_diff <- read.csv('/Users/darshak/AWS/YAML/Hot_diff.csv')

hot_diff_plot <- plot_ly(x = c(1:14), y = (hot_diff$HOT_DIFF_BP), name = "BP",type = "scatter", mode = c("markers", "lines")) %>% 
  add_trace(y = (hot_diff$HOT_DIFF_L), name = "LRUP", mode = 'lines+markers', color = list('red')) %>% 
  add_trace(y = (hot_diff$HOT_DIFF_DP), name = "DP", mode = 'lines+markers', color = list('red')) %>% 
  layout(title = "Cold To Hot Movement over 500 requests", xaxis = list(title = 'Time Points'), yaxis = list(title = 'Cold to Hot Expensive requests'))
hot_diff_plot


