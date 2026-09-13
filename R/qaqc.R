required_columns <- c("timestamp", "source_id", "variable", "value", "unit")

flag_observations <- function(data) {
  missing <- setdiff(required_columns, names(data))
  if (length(missing) > 0) stop(paste("missing columns:", paste(missing, collapse = ", ")))
  data$value_original <- data$value
  data$unit_original <- data$unit
  data$qa_flag <- "ok"
  data$qa_flag[is.na(data$value)] <- "missing_value"
  data$qa_flag[!is.na(data$value) & data$value < 0] <- "negative_value"
  gas_zero <- data$variable %in% c("ch4", "co2", "nh3") & !is.na(data$value) & data$value == 0
  data$qa_flag[gas_zero] <- "zero_concentration"
  data
}

apply_response_window <- function(data, response_seconds, flush_seconds) {
  if (response_seconds < 0 || flush_seconds < 0) stop("windows must be non-negative")
  data$response_seconds <- response_seconds
  data$flush_seconds <- flush_seconds
  data
}
