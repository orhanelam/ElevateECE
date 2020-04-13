// motor controller taking servo-style PWM signal as input and running an adafruit classic motor shield as output
// by Tyler Bletsch (2020-02-04)

//////////// motor stuff
#include <AFMotor.h>

AF_DCMotor motor3(3);
AF_DCMotor motor4(4);

AF_DCMotor motors[] = {motor3,motor4};
const int num_motors = sizeof(motors)/sizeof(*motors);

int time_min = 1000; // servo pulse us for full reverse
int time_max = 2000; // servo pulse us for full forward
int time_stop = 1500; // servo pulse us for stop
int time_deadzone = 100; // servo pulse deadzone around time_stop


/////////////// pwm reading stuff
int in_pins[] = {A0,A1}; // get servo pwm signals from here (note: i use direct port/pin manipulation elsewhere in code, so changing this will break stuff. )
const int num_in_pins = sizeof(in_pins)/sizeof(*in_pins);

unsigned long t_last_rise[num_in_pins] = {0};
bool state_last[num_in_pins] = {0};
int t_delta[num_in_pins] = {0};

byte old_portc=0;

// see https://playground.arduino.cc/Main/PinChangeInterrupt/ for info on this interrupt
// handle pin change interrupt for A0 to A5 here
ISR (PCINT1_vect) {
  //Serial.println("ok");
  unsigned long now = micros();
  byte portc_now = PINC;
  byte change = old_portc ^ portc_now;

  for (int i=0; i<num_in_pins; i++) {
    bool state = portc_now & (1<<i);
    bool state_last = old_portc & (1<<i);
    if (!state_last && state) { // rising edge
      t_last_rise[i] = now;
    } else if (state_last && !state) { // falling edge
      if (t_last_rise[i] != 0) { // non-first time
        t_delta[i] = now - t_last_rise[i];
      }
    }
  }
  old_portc = portc_now;
}  

void setup() {
  // pin setup and initialize
  for (int i=0; i<num_in_pins; i++) {
    pinMode(in_pins[i],INPUT_PULLUP);
    state_last[i] = digitalRead(in_pins[i]);
  }
  
  // pin change interrupt setup  (see https://playground.arduino.cc/Main/PinChangeInterrupt/ )
  PCMSK1 = 0b00001111; // A0-A3 enable
  PCIFR = 0b00000010; // clear any outstanding interrupt: PCMSK1 on, PCMSK0 and PCMSK2 off
  PCICR = 0b00000010; // enable interrupt: PCMSK1 on, PCMSK0 and PCMSK2 off

  // serial setup
  Serial.begin(115200);
  Serial.println("Booted.");
  
  // motor setup
  for (int m=0; m<num_motors; m++) {
    motors[m].run(RELEASE);
  }

} 

void loop() {
  // check time status and update motors and print status to serial
  for (int i=0; i<num_in_pins; i++) {
    if (t_last_rise[i]==0 || micros() - t_last_rise[i] > 30000) {
      Serial.print("x"); Serial.print(" ");
      motors[i].run(RELEASE);
    } else {
      Serial.print(t_delta[i]); Serial.print(" ");
      run_motor(i,t_delta[i]);
    }
  }
  Serial.println();
  delay(100);
}

// like map(), but output cant go outside of target bounds (clamped)
#define clampmap(x,a,b,u,v) max(min(map(x,a,b,u,v),v),u)

// run a motor based on a servo pwm time (t_delta in range time_min .. time_max)
void run_motor(int motor_num, int t_delta) {
  int i = motor_num;
  if (t_delta==0) {
    Serial.println("ERROR: t_delta is 0");
  } else if (t_delta < time_stop-time_deadzone) {
    motors[i].run(BACKWARD);
    motors[i].setSpeed(clampmap(t_delta,time_stop-time_deadzone,time_min,0,255));
  } else if (t_delta < time_stop+time_deadzone) {
    motors[i].run(FORWARD);
    motors[i].setSpeed(0);
  } else {
    motors[i].run(FORWARD);
    motors[i].setSpeed(clampmap(t_delta,time_stop+time_deadzone,time_max,0,255));
  }
}
