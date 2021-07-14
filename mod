Sub YIELD()

' Calculate IRR, Yield, and NAR

'   Clear Content
    Range("D5").Select
    Selection.ClearContents
    
'    Range("E1213:Z71").Select
'    Selection.ClearContents
    
    If Range("D10").Value = "Custom" Then
        Range("E13:AC72").Select
        Selection.ClearContents
    End If
    
    If Range("D10").Value <> "Custom" Then
        Range("B13:AC72").Select
        Selection.ClearContents
    End If
    
    Range("R9").Select
    
'   Calculate FV
    RunPython ("import CalculatingYield;CalculatingYield.IRR()")
    ' RunPython ("yield.IRR()")

    Range("R9").Select

End Sub


Sub YIELD_PORTFOLIO()

' Calculate IRR, Yield, and NAR

    Sheets("Conditional Rates").Activate
    Range("A2:L10000").Select
    Selection.ClearContents

'   Clear Content
    Sheets("Portfolio").Activate
    Range("B17:L50").Select
    Selection.ClearContents
    
    Range("D10").Select
            
'   Calculate IRRs
    RunPython ("import CalculatingYield;CalculatingYield.calculate_portfolio_irrs()")
    ' RunPython ("yield.IRR()")

    Range("D10").Select

End Sub


