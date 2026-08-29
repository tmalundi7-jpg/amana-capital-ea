Set WshShell = WScript.CreateObject("WScript.Shell")
AppPath = "C:\Users\tmalu\AppData\Local\Programs\antigravity\Antigravity.exe"

' Try to activate first (if it is already open)
Success = WshShell.AppActivate("Antigravity")

If Not Success Then
    ' Launch the app
    WshShell.Run """" & AppPath & """"
    
    ' Wait for the app to open and become active (loop up to 20 times, waiting 1 second each)
    For i = 1 To 20
        WScript.Sleep 1000
        If WshShell.AppActivate("Antigravity") Then
            Success = True
            ' Give it a few extra seconds to fully load its UI before pasting
            WScript.Sleep 4000 
            Exit For
        End If
    Next
End If

If Success Then
    ' Extra safety sleep to ensure input field is ready
    WScript.Sleep 1000
    WshShell.SendKeys "^v"
    WScript.Sleep 1000
    WshShell.SendKeys "{ENTER}"
End If
