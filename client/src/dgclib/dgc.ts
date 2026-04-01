import { DGC_IDS } from "./ids"


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

    // configuration options
    // configuration options will persist 
    //      through this.clear()
    // ------------------------------------------

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
            folders: folders
        })
    }


    // Allow the creation of text notes in the 
    // expressions list
    setNotes(notes: boolean): void {
        this.calculator.updateSettings({
            notes: notes
        })
    }


    // Allow the creation of sliders in the 
    // expressions list
    setSliders(sliders: boolean): void {
        this.calculator.updateSettings({
            sliders: sliders
        })
    }


    // // Allow the use of Actions. May be true, 
    // // false, or 'auto'. When true or false, 
    // // actions are completely enabled or 
    // // disabled. When 'auto', actions are 
    // // enabled, but some associated UI is only 
    // // displayed after the user enters a valid 
    // // action. In a future API version, 'auto' 
    // // may become a synonym for true.
    // setActions(actions: boolean): void {
    //     this.calculator.updateSettings({
    //         actions: actions
    //     })
    // }


    // Allow the use of "with" substitutions and 
    // list comprehensions
    setSubstitutions(substitutions: boolean): void {
        this.calculator.updateSettings({
            substitutions: substitutions
        })
    }


    // Allow hyperlinks in notes/folders, and 
    // links to help documentation in the 
    // expressions list (e.g. regressions with 
    // negative R2 values or plots with 
    // unresolved detail)
    setLinks(links: boolean): void {
        this.calculator.updateSettings({
            links: links
        })
    }


    // Display the keypad in QWERTY layout (false
    // shows an alphabetical layout)
    setQwertyKeyboard(qwertyKeyboard: boolean): void {
        this.calculator.updateSettings({
            qwertyKeyboard: qwertyKeyboard
        })
    }


    // Enable/disable functions related to 
    // univariate data visualizations, 
    // statistical distributions, and hypothesis 
    // testing
    setDistributions(distributions: boolean): void {
        this.calculator.updateSettings({
            distributions: distributions
        })
    }


    // Show a restricted menu of available 
    // functions
    setRestrictedFunctions(restrictedFunctions: boolean): void {
        this.calculator.updateSettings({
            restrictedFunctions: restrictedFunctions
        })
    }


    // Force distance and midpoint functions to 
    // be enabled, even if restrictedFunctions is
    // set to true. In that case the geometry 
    // functions will also be added to the the 
    // "Misc" keypad.
    setForceEnableGeometryFunctions(forceEnableGeometryFunctions: boolean): void {
        this.calculator.updateSettings({
            forceEnableGeometryFunctions: forceEnableGeometryFunctions
        })
    }


    // API v1.11 only: when true, enable the 
    // repeat function. In future API versions, 
    // this option will be removed and the repeat
    // function will be available 
    // unconditionally.
    setEnableRepeatFunction(enableRepeatFunction: boolean): void {
        this.calculator.updateSettings({
            enableRepeatFunction: enableRepeatFunction
        })
    }


    // Paste a valid desmos graph URL to import 
    // that graph
    setPasteGraphLink(pasteGraphLink: boolean): void {
        this.calculator.updateSettings({
            pasteGraphLink: pasteGraphLink
        })
    }


    // When true, clearing the graph through the 
    // UI or calling setBlank() will leave the 
    // calculator in degreeMode. Note that, if a 
    // default state is set, resetting the graph 
    // through the UI will result in the 
    // calculator's degreeMode matching the mode 
    // of that state, regardless of this option.
    setClearIntoDegreeMode(clearIntoDegreeMode: boolean): void {
        this.calculator.updateSettings({
            clearIntoDegreeMode: clearIntoDegreeMode
        })
    }


    // // The color palette that the calculator will
    // // cycle through. See the Colors section.
    // setColors(colors: ): void {
    //     this.calculator.updateSettings({
    //         colors: colors
    //     })
    // }


    // Determine whether the calculator should 
    // automatically resize whenever there are 
    // changes to element's dimensions. If set to
    // false you will need to explicitly call 
    // .resize() in certain situations. See 
    // .resize().
    setAutosize(autosize: boolean): void {
        this.calculator.updateSettings({
            autosize: autosize
        })
    }


    // Determine whether the calculator should
    // plot inequalities
    setPlotInequalities(plotInequalities: boolean): void {
        this.calculator.updateSettings({
            plotInequalities: plotInequalities
        })
    }


    // Determine whether the calculator should 
    // plot implicit equations and inequalities
    setPlotImplicits(plotImplicits: boolean): void {
        this.calculator.updateSettings({
            plotImplicits: plotImplicits
        })
    }


    // Determine whether the calculator should 
    // plot single-variable implicit equations
    setPlotSingleVariableImplicitEquations(plotSingleVariableImplicitEquations: boolean): void {
        this.calculator.updateSettings({
            plotSingleVariableImplicitEquations: plotSingleVariableImplicitEquations
        })
    }


    // When true, fonts and line thicknesses are 
    // increased to aid legibility.
    setProjectorMode(projectorMode: boolean): void {
        this.calculator.updateSettings({
            projectorMode: projectorMode
        })
    }


    // When true, users are able to toggle 
    // between decimal and fraction output in 
    // evaluations if Desmos detects a good 
    // rational approximation.
    setDecimalToFraction(decimalToFraction: boolean): void {
        this.calculator.updateSettings({
            decimalToFraction: decimalToFraction
        })
    }


    // Base font size.
    setFontSize(fontSize: number): void {
        this.calculator.updateSettings({
            fontSize: fontSize
        })
    }


    // Display the calculator with an inverted 
    // color scheme.
    setInvertedColors(invertedColors: boolean): void {
        this.calculator.updateSettings({
            invertedColors: invertedColors
        })
    }


    // Language. See the Languages section for 
    // more information.
    setLanguage(language: string): void {
        this.calculator.updateSettings({
            language: language
        })
    }


    // Set the input and output Braille code for 
    // persons using refreshable Braille 
    // displays. Valid options are 'nemeth', 
    // 'ueb', or 'none'.
    setBrailleMode(brailleMode: string): void {
        this.calculator.updateSettings({
            brailleMode: brailleMode
        })
    }


    // Allow users to write six-dot Braille 
    // characters using the Home Row keys 
    // (S, D, F, J, K, and L). Requires that 
    // brailleMode be 'nemeth' or 'ueb'.
    setSixKeyInput(sixKeyInput: boolean): void {
        this.calculator.updateSettings({
            sixKeyInput: sixKeyInput
        })
    }


    // Show Braille controls in the settings menu
    // and enable shortcut keys for switching 
    // between Braille modes. See Accessibility 
    // Notes.
    setBrailleControls(brailleControls: boolean): void {
        this.calculator.updateSettings({
            brailleControls: brailleControls
        })
    }


    // Permit the calculator to generate sound, 
    // including using the tone method and in 
    // Audio Trace. See Accessibility Notes.
    setAudio(audio: boolean): void {
        this.calculator.updateSettings({
            audio: audio
        })
    }


    // Manually set a description for the graph 
    // canvas (which replaces the automatically 
    // generated text we create). Set to an empty
    // string to remove the description entirely,
    // or undefined to restore the generated 
    // text. See Accessibility Notes.
    setGraphDescription(graphDescription: string): void {
        this.calculator.updateSettings({
            graphDescription: graphDescription
        })
    }


    // When true, tables and distributions will 
    // display an icon that allows the user to 
    // automatically snap the viewport to 
    // appropriate bounds for viewing that 
    // expression.
    setZoomFit(zoomFit: boolean): void {
        this.calculator.updateSettings({
            zoomFit: zoomFit
        })
    }


    // When true, all linearizable regression 
    // models will have log mode enabled by 
    // default, and the checkbox used to toggle 
    // log mode will be hidden from the 
    // expression interface. See this support 
    // article for more information.
    setForceLogModeRegressions(forceLogModeRegressions: boolean): void {
        this.calculator.updateSettings({
            forceLogModeRegressions: forceLogModeRegressions
        })
    }


    // When true, all linearizable regression 
    // models will have log mode enabled by 
    // default, but, unlike 
    // forceLogModeRegressions, the checkbox used
    // to toggle log mode will be visible from 
    // the expression interface. See this support 
    // article for more information.
    setDefaultLogModeRegressions(defaultLogModeRegressions: boolean): void {
        this.calculator.updateSettings({
            defaultLogModeRegressions: defaultLogModeRegressions
        })
    }


    // When true, users can create arbitrary 
    // regression models using expression syntax.
    // See this article on regressions.
    setCustomRegressions(customRegressions: boolean): void {
        this.calculator.updateSettings({
            customRegressions: customRegressions
        })
    }


    // When true, users can create regressions 
    // from a fixed menu of model options from 
    // the table column interface. See this 
    // article on regressions.
    setRegressionTemplates(regressionTemplates: boolean): void {
        this.calculator.updateSettings({
            regressionTemplates: regressionTemplates
        })
    }


    // When true, the option to use logarithmic 
    // axis scales is enabled.
    setLogScales(logScales: boolean): void {
        this.calculator.updateSettings({
            logScales: logScales
        })
    }


    // When true, the tone command is enabled.
    setTone(tone: boolean): void {
        this.calculator.updateSettings({
            tone: tone
        })
    }

    
    // When true, the syntax for interval 
    // comprehensions is enabled.
    setIntervalComprehensions(intervalComprehensions: boolean): void {
        this.calculator.updateSettings({
            intervalComprehensions: intervalComprehensions
        })
    }


    // Globally mute or unmute sound generated by 
    // the calculator's built-in tone() function. 
    // See the section on tones below.
    setMuted(muted: boolean): void {
        this.calculator.updateSettings({
            muted: muted
        })
    }


    // Enable the "Complex Mode" toggle in the 
    // Settings Menu. See section on complex 
    // numbers.
    setAllowComplex(allowComplex: boolean): void {
        this.calculator.updateSettings({
            allowComplex: allowComplex
        })
    }


    // Specify how the calculator reports object 
    // positions to screen readers. Valid options 
    // are 'coordinates', 'percents', or 
    // 'default'. If set to 'default', objects 
    // will be reported in terms of X and Y 
    // coordinates if eeither X or Y axis is 
    // visible. If both axes are hidden, 
    // positions are reported as percentages from 
    // the viewport's top and left edges.
    setReportPosition(reportPosition: string): void {
        this.calculator.updateSettings({
            reportPosition: reportPosition
        })
    }


    // When true, show a button next to 
    // expression evaluations that copies the 
    // evaluation LaTeX to the system clipboard. 
    // Optionally, it is possible to define a 
    // callback that provides custom copy logic, 
    // e.g., for an application that manages its 
    // own clipboard. See the 
    // onEvaluationCopyClick entry below.
    setShowEvaluationCopyButtons(showEvaluationCopyButtons: boolean): void {
        this.calculator.updateSettings({
            showEvaluationCopyButtons: showEvaluationCopyButtons
        })
    }


    // // A function (string) -> void that will be 
    // // invoked when the user clicks an expression 
    // // evaluation's copy button (see above) with 
    // // the evaluation LaTeX as its argument. The 
    // // default implementation copies to the 
    // // system clipboard.
    // setOnEvaluationCopyClick(onEvaluationCopyClick: ): void {
    //     this.calculator.updateSettings({
    //         onEvaluationCopyClick: onEvaluationCopyClick
    //     })
    // }


    // When true, allow the use of recursive 
    // functions. See the article on recursion 
    // for more information.
    setRecursion(recursion: boolean): void {
        this.calculator.updateSettings({
            recursion: recursion
        })
    }


    // graph settings
    // graph settings will be overwritten on 
    //      this.clear()
    // ------------------------------------------

    // When true, trig functions assume arguments 
    // are in degrees. Otherwise, arguments are 
    // assumed to be in radians.
    setDegreeMode(degreeMode: boolean): void {
        this.calculator.updateSettings({
            degreeMode: degreeMode
        })
    }


    // Show or hide grid lines on the graph 
    // paper.
    setShowGrid(showGrid: boolean): void {
        this.calculator.updateSettings({
            showGrid: showGrid
        })
    }


    // When true, use a polar grid. Otherwise, 
    // use cartesian grid.
    setPolarMode(polarMode: boolean): void {
        this.calculator.updateSettings({
            polarMode: polarMode
        })
    }


    // Show or hide the x axis.
    setShowXAxis(showXAxis: boolean): void {
        this.calculator.updateSettings({
            showXAxis: showXAxis
        })
    }


    // Show or hide the y axis.
    setShowYAxis(showYAxis: boolean): void {
        this.calculator.updateSettings({
            showYAxis: showYAxis
        })
    }


    // Show or hide numeric tick labels on the x 
    // axis.
    setXAxisNumbers(xAxisNumbers: boolean): void {
        this.calculator.updateSettings({
            xAxisNumbers: xAxisNumbers
        })
    }


    // Show or hide numeric tick labels on the y 
    // axis.
    setYAxisNumbers(yAxisNumbers: boolean): void {
        this.calculator.updateSettings({
            yAxisNumbers: yAxisNumbers
        })
    }


    // Show or hide numeric tick labels at 
    // successive angles. Only relevant when 
    // polarMode is true.
    setPolarNumbers(polarNumbers: boolean): void {
        this.calculator.updateSettings({
            polarNumbers: polarNumbers
        })
    }


    // Spacing between numeric ticks on the x 
    // axis. Will be ignored if set too small to 
    // display. When set to 0, tick spacing is 
    // chosen automatically.
    setXAxisStep(xAxisStep: number): void {
        this.calculator.updateSettings({
            xAxisStep: xAxisStep
        })
    }


    // Spacing between numeric ticks on the y 
    // axis. Will be ignored if set too small to 
    // display. When set to 0, tick spacing is 
    // chosen automatically.
    setYAxisStep(yAxisStep: number): void {
        this.calculator.updateSettings({
            yAxisStep: yAxisStep
        })
    }


    // Subdivisions between ticks on the x axis. 
    // Must be an integer between 0 and 5. 1 
    // means that only the major grid lines will 
    // be shown. When set to 0, subdivisions are 
    // chosen automatically.
    setXAxisMinorSubdivisions(xAxisMinorSubdivisions: number): void {
        this.calculator.updateSettings({
            xAxisMinorSubdivisions: xAxisMinorSubdivisions
        })
    }


    // Subdivisions between ticks on the y axis. 
    // Must be an integer between 0 and 5. 1 
    // means that only the major grid lines will 
    // be shown. When set to 0, subdivisions are 
    // chosen automatically.
    setYAxisMinorSubdivisions(yAxisMinorSubdivisions: number): void {
        this.calculator.updateSettings({
            yAxisMinorSubdivisions: yAxisMinorSubdivisions
        })
    }


    // // Determines whether to place arrows at one 
    // // or both ends of the x axis. See Axis Arrow
    // // Modes.
    // setXAxisArrowMode(xAxisArrowMode: ): void {
    //     this.calculator.updateSettings({
    //         xAxisArrowMode: xAxisArrowMode
    //     })
    // }


    // // Determines whether to place arrows at one 
    // // or both ends of the y axis. See Axis Arrow
    // // Modes.
    // setYAxisArrowMode(yAxisArrowMode: ): void {
    //     this.calculator.updateSettings({
    //         yAxisArrowMode: yAxisArrowMode
    //     })
    // }
    

    // Label placed below the x axis.
    setXLabel(xAxisLabel: string): void {
        this.calculator.updateSettings({
            xAxisLabel: xAxisLabel
        })
    }


    // Label placed beside the y axis.
    setYLabel(yAxisLabel: string): void {
        this.calculator.updateSettings({
            yAxisLabel: yAxisLabel
        })
    }


    // Scale of the x axis.
    setXAxisScale(xAxisScale: string): void {
        this.calculator.updateSettings({
            xAxisScale: xAxisScale
        })
    }


    // Scale of the y axis.
    setYAxisScale(yAxisScale: string): void {
        this.calculator.updateSettings({
            yAxisScale: yAxisScale
        })
    }


    // Global random seed used for generating 
    // values from the calculator's built-in 
    // random() function. See the section on 
    // random seeds below.
    setRandomSeed(randomSeed: string): void {
        this.calculator.updateSettings({
            randomSeed: randomSeed
        })
    }

    
    // behaviour methods
    // ------------------------------------------

    // fit methods
    // -----------------

    fitExponential(): void {
        if(!this.calculator)        return
        if(this.exprv.length === 0) return

        this.calculator.setExpression({
            id:    DGC_IDS.FIT_EXPONENTIAL,
            latex: `y_1~ab^{x_1}`
        })
    }


    clearExponential(): void {
        if(!this.calculator)        return
        if(this.exprv.length === 0) return

        Object.values(DGC_IDS)
            .filter(id => id.startsWith(DGC_IDS.FIT_EXPONENTIAL))
            .forEach(id => this.calculator.removeExpression({ id }))
    }


    fitLinear(): void {
        if(!this.calculator)        return
        if(this.exprv.length === 0) return

        this.calculator.setExpression({
            id:    DGC_IDS.FIT_LINEAR,
            latex: 'y_1~mx_1+b'
        })
    }


    clearLinear(): void {
        if(!this.calculator)        return
        if(this.exprv.length === 0) return

        Object.values(DGC_IDS)
            .filter(id => id.startsWith(DGC_IDS.FIT_LINEAR))
            .forEach(id => this.calculator.removeExpression({ id }))
    }

    
    fitLogarithmic(): void {
        if(!this.calculator)        return
        if(this.exprv.length === 0) return

        this.calculator.setExpression({
            id:    DGC_IDS.FIT_LOGARITHMIC,
            latex: `y_1~a\\ln(x_1)+b`
        })
    }


    clearLogarithmic(): void {
        if(!this.calculator)        return
        if(this.exprv.length === 0) return

        Object.values(DGC_IDS)
            .filter(id => id.startsWith(DGC_IDS.FIT_LOGARITHMIC))
            .forEach(id => this.calculator.removeExpression({ id }))
    }

    
    fitLogistic(): void {
        if(!this.calculator)        return
        if(this.exprv.length === 0) return

        this.calculator.setExpression({
            id:    DGC_IDS.FIT_LOGISTIC,
            latex: `y_1~\\frac{L}{1+e^{-k(x_1-x_0)}}`
        })
    }


    clearLogistic(): void {
        if(!this.calculator)        return
        if(this.exprv.length === 0) return

        Object.values(DGC_IDS)
            .filter(id => id.startsWith(DGC_IDS.FIT_LOGISTIC))
            .forEach(id => this.calculator.removeExpression({ id }))
    }


    fitPolynomial(degree: number): void {
        if(!this.calculator)        return
        if(this.exprv.length === 0) return

        const terms = Array.from({ length: degree + 1 }, (_, i) => {
            const power = degree - i
            const coeff = String.fromCharCode(97 + i) // a, b, c, ...
            return power === 0 ? coeff
                : power === 1 ? `${coeff}x_1`
                :               `${coeff}x_1^{${power}}`
        }).join('+')

        this.calculator.setExpression({
            id:    DGC_IDS.FIT_POLYNOMIAL,
            latex: `y_1~${terms}`
        })
    }


    clearPolynomial(): void {
        if(!this.calculator)        return
        if(this.exprv.length === 0) return

        Object.values(DGC_IDS)
            .filter(id => id.startsWith(DGC_IDS.FIT_POLYNOMIAL))
            .forEach(id => this.calculator.removeExpression({ id }))
    }


    fitPower(): void {
        if(!this.calculator)        return
        if(this.exprv.length === 0) return

        this.calculator.setExpression({
            id:    DGC_IDS.FIT_POWER,
            latex: `y_1~ax_1^{b}`
        })
    }


    clearPower(): void {
        if(!this.calculator)        return
        if(this.exprv.length === 0) return

        Object.values(DGC_IDS)
            .filter(id => id.startsWith(DGC_IDS.FIT_POWER))
            .forEach(id => this.calculator.removeExpression({ id }))
    }


    fitSinusoidal(): void {
        if(!this.calculator)        return
        if(this.exprv.length === 0) return

        this.calculator.setExpression({
            id:    DGC_IDS.FIT_SINUSOIDAL,
            latex: `y_1~a\\sin(bx_1+c)+d`
        })
    }


    clearSinusoidal(): void {
        if(!this.calculator)        return
        if(this.exprv.length === 0) return

        Object.values(DGC_IDS)
            .filter(id => id.startsWith(DGC_IDS.FIT_SINUSOIDAL))
            .forEach(id => this.calculator.removeExpression({ id }))
    }


    clearFit(): void {
        if(!this.calculator) return

        Object.values(DGC_IDS)
            .filter(id => id.startsWith('fit-'))
            .forEach(id => this.calculator.removeExpression({ id }))
    }


    hasFit(target_id: string): boolean {
        if(!this.calculator) return false

        return this.calculator.getExpressions()
            .some((expr: ReturnType<typeof this.calculator.getExpressions>[number]) => expr.id?.startsWith(target_id))
    }


    // core methods
    // -----------------

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
                { latex: 'x_1', values: x },
                { latex: 'y_1', values: y }
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