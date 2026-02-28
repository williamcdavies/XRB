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


    // Show the graphpaper
    setGraphPaper(graphPaper: boolean): void {
        this.calculator.updateSettings({
            graphPaper: graphPaper
        })
    }


    // Show the expressions list
    setExpressions(expressions: boolean): void {
        this.calculator.updateSettings({
            expressions: expressions
        })
    }


    // Show the settings wrench, for changing 
    // graph display. See Accessibility Notes.
    setSettingsMenu(settingsMenu: boolean): void {
        this.calculator.updateSettings({
            settingsMenu: settingsMenu
        })
    }


    // Show onscreen zoom buttons
    setZoomButtons(zoomButtons: boolean): void {
        this.calculator.updateSettings({
            zoomButtons: zoomButtons
        })
    }


    // Show the onscreen keypad
    setKeypad(keypad: boolean): void {
        this.calculator.updateSettings({
            keypad: keypad
        })
    }


    // When false, the keypad will start out 
    // minimized, and the user needs to manually 
    // open it. When true, the onscreen keypad 
    // will be opened anytime focus is in a math 
    // input. Note: this option is ignored if we 
    // detect that the user is on a touch device. 
    // In that case, the keypad is always activated.
    setKeypadActivated(keypadActivated: boolean): void {
        this.calculator.updateSettings({
            keypadActivated: keypadActivated
        })
    }


    // API v1.11 only: when true, display a 
    // control allowing the onscreen keypad to be
    // minimized when the calculator is narrow 
    // enough that the graphpaper is stacked 
    // above the expression list. This control is
    // not displayed on touch screen devices 
    // where the onscreen keypad is necessary for
    // editing. In future versions of the API, 
    // this behavior will be enabled 
    // unconditionally and the option will be 
    // removed.
    setAllowKeypadToBeDismissedWhenNarrow(allowKeypadToBeDismissedWhenNarrow: boolean): void {
        this.calculator.updateSettings({
            allowKeypadToBeDismissedWhenNarrow: allowKeypadToBeDismissedWhenNarrow
        })
    }


    // If a default state is set, show an 
    // onscreen reset button
    setShowResetButtonOnGraphpaper(showResetButtonOnGraphpaper: boolean): void {
        this.calculator.updateSettings({
            showResetButtonOnGraphpaper: showResetButtonOnGraphpaper
        })
    }


    // Show the bar on top of the expressions 
    // list
    setExpressionsTopbar(expressionsTopbar: boolean): void {
        this.calculator.updateSettings({
            expressionsTopbar: expressionsTopbar
        })
    }


    // Show Points of Interest (POIs) as gray 
    // dots that can be clicked on
    setPointsOfInterest(pointsOfInterest: boolean): void {
        this.calculator.updateSettings({
            pointsOfInterest: pointsOfInterest
        })
    }


    // Allow tracing curves to inspect 
    // coordinates, and showing point coordinates
    // when clicked
    setTrace(trace: boolean): void {
        this.calculator.updateSettings({
            trace: trace
        })
    }


    // Add a subtle 1px gray border around the 
    // entire calculator
    setBorder(border: boolean): void {
        this.calculator.updateSettings({
            border: border
        })
    }


    // Disable user panning and zooming graphpaper
    setLockViewport(lockViewport: boolean): void {
        this.calculator.updateSettings({
            lockViewport: lockViewport
        })
    }


    // Collapse the expressions list
    setExpressionsCollapsed(expressionsCollapsed: boolean): void {
        this.calculator.updateSettings({
            expressionsCollapsed: expressionsCollapsed
        })
    }
    

    // Limit the size of an expression to 500 
    // LaTeX tokens and a maximum nesting depth 
    // of 30
    setCapExpressionSize(capExpressionSize: boolean): void {
        this.calculator.updateSettings({
            capExpressionSize: capExpressionSize
        })
    }


    // Enable features intended for content 
    // authoring
    setAuthorFeatures(authorFeatures: boolean): void {
        this.calculator.updateSettings({
            authorFeatures: authorFeatures
        })
    }


    // Allow adding images
    setImages(images: boolean): void {
        this.calculator.updateSettings({
            images: images
        })
    }


    // // Specify custom processing for 
    // // user-uploaded images
    // setImageUploadCallback(imageUploadCallback: ): void {
    //     this.calculator.updateSettings({
    //         imageUploadCallback: imageUploadCallback
    //     })
    // }


    // Allow the creation of folders in the 
    // expressions list
    setFolders(folders: boolean): void {
        this.calculator.updateSettings({
            images: folders
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