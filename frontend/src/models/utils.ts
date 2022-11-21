export interface Pagination<T> {
  links: {
    next: string
    previous: string
  }
  count: number
  total_pages: number
  results: T[]
}

export interface ApiError {
  detail: string
}

export interface Statistic {
  organizations: number
  users: number
  transactions: number
}
