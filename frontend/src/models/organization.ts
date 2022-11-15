export interface Organization {
  id: number
  name: string
  hashed_key: string
  count: number
  status: string
  created_at: Date
  deleted_at: Date | null
}

export enum Status {
  active = 'active',
  blocked = 'blocked',
}
