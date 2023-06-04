for /l %%x in (1, 1, 2000) do (
	adb shell input swipe 930 1485 100 1485 100
	timeout 2
)