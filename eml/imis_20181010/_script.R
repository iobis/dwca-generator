datasets <- read.csv("datasets.csv", sep = ";", stringsAsFactors = FALSE)

for (i in 1:nrow(datasets)) {
  if (!is.na(datasets$dasid[i])) {
    message(datasets$name[i])
    file.rename(paste0("imis_dasid_", datasets$dasid[i]), datasets$name[i])
  }
}
