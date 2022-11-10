export interface Pagination<T> {
  links: {
    next: string
    previous: string
  }
  count: number
  total_pages: number
  results: T[]
}
