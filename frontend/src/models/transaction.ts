export interface Transaction {
  id: number
  organization: number
  amount: number
  created_at: Date
  deleted_at: Date | null
}

