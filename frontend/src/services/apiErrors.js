export const getApiErrorMessage = (error, fallback = "Something went wrong.") =>
  error.response?.data?.detail || error.message || fallback;