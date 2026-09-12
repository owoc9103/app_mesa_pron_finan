# Descarga las bases FPP3 y las deja como CSV tidy (fecha + variables).
base_url <- "https://raw.githubusercontent.com/robjhyndman/fpp3/master/data"
args <- commandArgs(trailingOnly = FALSE)
script <- sub("^--file=", "", args[grep("^--file=", args)])
root <- if (length(script)) dirname(normalizePath(script)) else getwd()
out_dir <- file.path(root, "data")
rda_dir <- file.path(out_dir, "_rda")
dir.create(rda_dir, showWarnings = FALSE, recursive = TRUE)

nombres <- c(
  "aus_accommodation", "aus_airpassengers", "aus_arrivals", "aus_births",
  "aus_fertility", "aus_inbound", "aus_migration", "aus_mortality",
  "aus_outbound", "aus_tobacco", "aus_vehicle_sales", "boston_marathon",
  "canadian_gas", "guinea_rice", "insurance", "melb_walkers",
  "nsw_offences", "ny_childcare", "otexts_views", "prices",
  "souvenirs", "us_change", "us_employment", "us_gasoline"
)

freq_label <- function(iv) {
  if (is.null(iv)) return("desconocida")
  if (isTRUE(iv$year > 0)) return("anual")
  if (isTRUE(iv$quarter > 0)) return("trimestral")
  if (isTRUE(iv$month > 0)) return("mensual")
  if (isTRUE(iv$week > 0)) return("semanal")
  if (isTRUE(iv$day > 0)) return("diaria")
  "desconocida"
}

index_to_date <- function(idx, iv) {
  if (is.numeric(idx) && !inherits(idx, "yearmonth") && !inherits(idx, "yearquarter") &&
      !inherits(idx, "yearweek") && isTRUE(iv$year > 0)) {
    return(as.Date(sprintf("%04d-01-01", as.integer(idx))))
  }
  if (inherits(idx, "Date")) return(idx)
  as.Date(as.numeric(idx), origin = "1970-01-01")
}

meta <- list()
for (nm in nombres) {
  dest <- file.path(rda_dir, paste0(nm, ".rda"))
  if (!file.exists(dest) || file.info(dest)$size < 100) {
    ok <- tryCatch({
      download.file(file.path(base_url, paste0(nm, ".rda")), dest, mode = "wb", quiet = TRUE)
      TRUE
    }, error = function(e) FALSE)
    if (!ok) {
      cat("FALLO descarga:", nm, "\n")
      next
    }
  }
  e <- new.env()
  ok <- tryCatch({ load(dest, envir = e); TRUE }, error = function(e) FALSE)
  if (!ok) {
    cat("FALLO load:", nm, "\n")
    next
  }
  x <- e[[ls(e)[1]]]
  iv <- attr(x, "interval")
  idx_name <- attr(x, "index")[1]
  df <- as.data.frame(x, stringsAsFactors = FALSE)
  if (!is.null(idx_name) && idx_name %in% names(df)) {
    df$fecha <- index_to_date(x[[idx_name]], iv)
    df[[idx_name]] <- NULL
  } else {
    df$fecha <- seq_len(nrow(df))
  }
  # fecha primero
  otras <- setdiff(names(df), "fecha")
  df <- df[c("fecha", otras)]
  csv <- file.path(out_dir, paste0(nm, ".csv"))
  write.csv(df, csv, row.names = FALSE, na = "")
  meta[[nm]] <- list(
    n = nrow(df),
    cols = paste(names(df), collapse = "|"),
    freq = freq_label(iv)
  )
  cat("OK", nm, "n=", nrow(df), "freq=", freq_label(iv), "\n")
}

cat("\nListo.\n")
