# 本番運用用
T.B.D
# デバッグ用
## emg_serial.py
Arduinoからシリアル経由でアナログ値を受け取り、プロットするプログラム
```bash
python emg_serial.py (sample)
```
sample: サンプリング数、省略時は2048  
プログラム内でシリアルデバイス名を直書しているため、USBデバイス名が異なる場合は以下の箇所を所望のデバイス名に書き換えること
```python
ser = serial.Serial('/dev/tty.usbmodem1141301', 115200, timeout=None)
```
