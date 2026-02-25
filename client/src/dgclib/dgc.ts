export class DesmosGraphingCalculator {
    private calculator: any
    
    private exprv:      string[]
    private exprc:      number
    

    constructor(elt: HTMLElement, options?: any) {
        if(!(window as any).Desmos) {
            throw new Error
        }

        this.calculator = new (window as any).Desmos.GraphingCalculator(
            elt,
            options
        )

        this.exprv      = []
        this.exprc      = 0
    }


    setGraphPaper(graphPaper: boolean): void {
        this.calculator.updateSettings({
            graphPaper: graphPaper
        })
    }


    setExpressions(expressions: boolean): void {
        this.calculator.updateSettings({
            expressions: expressions
        })
    }


    setSettingsMenu(settingsMenu: boolean): void {
        this.calculator.updateSettings({
            settingsMenu: settingsMenu
        })
    }


    setXLabel(xAxisLabel: string): void {
        this.calculator.updateSettings({
            xAxisLabel: xAxisLabel
        })
    }


    setYLabel(yAxisLabel: string): void {
        this.calculator.updateSettings({
            yAxisLabel: yAxisLabel
        })
    }

    // add new dataset
    add(x: number[], 
        y: number[]): void {
        if(!this.calculator)                 return
        if(x.length === 0 || y.length === 0) return
        if(x.length !== y.length)            return

        const id = `dataset-${ this.exprc }`
        
        this.calculator.setExpression({
            id,
            type: 'table',
            columns: [
                { latex: 'x', values: x },
                { latex: 'y', values: y }
            ]
        })

        this.exprv.push(id)
        ++this.exprc
    }


    // load new dataset
    //  overrides existing dataset
    //  overrides existing expressions
    load(x:      number[], 
         y:      number[], 
         xAxisLabel: string = "X", 
         yAxisLabel: string = "Y"): void {
        if(!this.calculator)                 return
        if(x.length === 0 || y.length === 0) return
        if(x.length !== y.length)            return

        this.clear()
        this.add(x, y)
        this.setXLabel(xAxisLabel)
        this.setYLabel(yAxisLabel)
    }


    clear(): void {
        if(!this.calculator) return

        this.exprv      = []
        this.exprc      = 0
        this.calculator.setBlank()
    }


    destroy(): void {
        if(!this.calculator) return

        this.clear()
        this.calculator.destroy()
        this.calculator = null
    }
}