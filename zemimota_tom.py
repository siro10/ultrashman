from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
import RPi.GPIO as GPIO
import sys
import time

# モーター制御用ピン
IN1 = 27
IN2 = 22
# SG90のピン設定
SERVO_PIN = 17  # SG90-1

MIN_DEGREE = -90       # 000 : -90degree
MAX_DEGREE = 90       # 180 : +90degree

# 設定値
#rotation_time = 10  # モーターを回転させる時間（秒）

# GPIO初期化
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)

def stop_motor_and_servo(servo):
    # モーター停止
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    # サーボをニュートラル位置に戻す
    if servo:
        servo.angle = 0
        sleep(1.0)
    print("モーターとサーボを停止しました。")

def move_motor(servo):
    # モーターを正転させる
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    sleep(rotation_time)

    # モーター停止
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    sleep(2)  # 停止後の待機時間
    
    servo.angle = 40  #ちょうど90度回転する
    sleep(2.0)
    servo.angle = 0　　#初期値に戻る
    sleep(2.0)
    
    # モーターを逆転させる
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    sleep(rotation_time)

    # モーター停止
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)


def main():
    # 初期化
    factory = PiGPIOFactory()
    # min_pulse_width, max_pulse_width, frame_width =>SG90仕様
    servo = AngularServo(SERVO_PIN, min_angle=MIN_DEGREE, max_angle=MAX_DEGREE, 
                         min_pulse_width=1/1000, max_pulse_width=2/1000, frame_width=1/50,
                         pin_factory=factory)
    
    try:
        print("モーター制御プログラムを開始します。")
        print("指定したキーを入力してください。")
        print("'s'を入力するとモーターが動きます。")
        print("'q'を入力するとプログラムを終了します。")

        while True:
            # キーボード入力を1文字読み取る
            c = sys.stdin.read(1)

            if c == 's':
                rotation_time = 10  # モーターを回転させる時間（秒）
                print("モーターを10秒動かします。")
                move_motor(servo)

            elif c == 'q':
                print("プログラムを終了します。")
                break

    except KeyboardInterrupt:
        print("強制終了やで。")

    finally:
        stop_motor_and_servo(servo)
        GPIO.cleanup()
        print("GPIOをクリーンアップしました。")

if __name__ == "__main__":
   main()
