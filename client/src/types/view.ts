import type { Table } from './table'

export type FitState = {
    linear:          boolean
    exponential:     boolean
    logarithmic:     boolean
    logistic:        boolean
    polynomial:      boolean
    polynomialDegree?: number
    power:           boolean
    sinusoidal:      boolean
}

export type Viewport = Record<string, number>

export type DocumentView = {
    id:              string
    name:            string
    table:           Table
    hiddenRows:      number[]
    xColumn:         string | null
    yColumn:         string | null
    aColumn:         string | null
    fits:            FitState
    viewport?:       Viewport | null
    savedAt:         number
    lastAccessedAt?: number
}
