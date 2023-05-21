for /l %%x in (1, 1, 20) do (
	echo "ignore existing gift"
	adb shell input tap 520 1220
	timeout 4
	adb shell input tap 520 2130
	timeout 2
	echo "sending gift"
	adb shell input tap 180 1810
	timeout 1
	adb shell input tap 500 840
	echo "adding sticker"
	timeout 2
	adb shell input tap 500 1725
	timeout 2
	adb shell input tap 770 1285
	timeout 1
	adb shell input tap 130 1650
	echo "send gift"
	timeout 2
	adb shell input tap 500 1940
	timeout 5
	echo "go to next friend"
	adb shell input swipe 930 1485 100 1485 100
	timeout 2
)