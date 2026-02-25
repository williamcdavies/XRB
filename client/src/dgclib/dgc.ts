export class DesmosGraphingCalculator {
    private calculator: any
    

    constructor(elt: HTMLElement, options?: any) {
        if(!(window as any).Desmos) {
            throw new Error
        }

        this.calculator = new (window as any).Desmos.GraphingCalculator(
            elt,
            options
        )
    }


    setXLabel(xLabel: string): void {
        this.calculator.updateSettings({
            xAxisLabel: xLabel
        })
    }


    setYLabel(yLabel: string): void {
        this.calculator.updateSettings({
            yAxisLabel: yLabel
        })
    }

    populate(x:      number[], 
             y:      number[], 
             xLabel: string, 
             yLabel: string): void {
        if(!this.calculator)                 return
        if(x.length === 0 || y.length === 0) return
        if(x.length !== y.length)            return

        this.calculator.setExpression({
            id: 'dataset',
            type: 'table',
            columns: [
                { latex: 'x', values: x },
                { latex: 'y', values: y }
            ]
        })

        this.setXLabel(xLabel)
        this.setYLabel(yLabel)
    }


    clear(): void {
        if(!this.calculator) return

        this.calculator.setBlank()
    }


    destroy(): void {
        if(!this.calculator) return

        this.calculator.destroy()
        this.calculator = null
    }
}