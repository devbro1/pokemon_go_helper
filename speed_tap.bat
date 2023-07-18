for /l %%x in (1, 1, 10000) do (
	
	adb shell input tap 520 2050
	adb shell input tap 520 2050
	adb shell input tap 520 2050
	adb shell input tap 520 2050
	adb shell input tap 520 2050
	adb shell input tap 330 2050
	timeout 1	
)


adb shell input tap 750 2050