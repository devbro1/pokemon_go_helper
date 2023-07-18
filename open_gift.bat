for /l %%x in (1, 1, 20) do (
	adb shell input tap 540 1650
	timeout 3
	adb shell input tap 960 1920
	timeout 1
	adb shell input tap 520 1920
	timeout 15
	adb shell input swipe 930 1485 100 1485 100
	timeout 1
)