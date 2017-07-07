// include the library code:
#include <LiquidCrystal.h>

// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);
const    int  switchPin        = 6;
const    long REFRESH_INTERVAL = 1000; //A Second
const    long GAME_TIME        = 80;
         long TIME_LEFT        = GAME_TIME;
         
int switchState = 0;
int clicks      = -1;
int prevState   = 0;
int started     = 0;
int highscore   = 0;

void setup() {
  lcd.begin(16, 2);
  Serial.begin(9600);

  pinMode(switchPin, INPUT);
  StartScreen();
}

void StartScreen()
{//Start screen
  lcd.clear();
  lcd.print("Counter game");
  lcd.setCursor(0, 1);
  lcd.print("You have ");
  lcd.print(TIME_LEFT / 60);
  lcd.print(":");
  if(TIME_LEFT < 10) //singles digit
    lcd.print("0");
  if(TIME_LEFT < 70 && TIME_LEFT > 59){ //special case for 60-69secs
    lcd.print("0");
    lcd.print(TIME_LEFT % 60);
  }else{
    lcd.print(TIME_LEFT % 60);
  }
  lcd.print("!");
}

int Timer(int reset)
{ //timer, reset resets start time
  static long          lastRefreshTime = 0;
  static unsigned long starttime       = millis();
  if(reset)
    starttime = millis();
  if(!TIME_LEFT)
      return 1;
  if(millis() - lastRefreshTime >= REFRESH_INTERVAL){ //Updated TIME_LEFT every second
      TIME_LEFT       -= 1;
      //I do this for delay of time if game not started right away
      while(millis() - (lastRefreshTime += REFRESH_INTERVAL) >= REFRESH_INTERVAL){
      }
  }
      
  PrintTimer();

  return 0;
}

void PrintTimer()
{ //Prints timer
  lcd.setCursor(0,0);
  lcd.print("Time Left - ");
  lcd.print(TIME_LEFT / 60);
  lcd.print(":");
  if(TIME_LEFT < 10)
    lcd.print("0");
  if(TIME_LEFT < 70 && TIME_LEFT > 59){
    lcd.print("0");
    lcd.print(TIME_LEFT % 60);
  }else{
    lcd.print(TIME_LEFT % 60);
  }
}

int ClickRegistered()
{ //Watches for state change (click)
    switchState = digitalRead(switchPin);
    if(switchState != prevState){
      if(switchState == LOW){
        prevState = switchState;
        return 1;
      }
    }
    prevState = switchState;
    return 0;
}

void FinishedScreen()
{
    int curr_count = 0;
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("Your score: ");
    lcd.print(clicks);
    lcd.setCursor(0,1);
    lcd.print("HighScore: ");
    if(highscore < clicks)
      highscore = clicks;
    lcd.print(highscore);
    delay(5000);
    lcd.clear();
    TIME_LEFT = 10;
    lcd.setCursor(0,1);
    lcd.print("Again? 2 clicks");
    int reset = 1;
    while(!Timer(reset) && !(curr_count == 2)){//two click event listner
      if(reset == 1)
        reset = 0;

      if(ClickRegistered())
        curr_count++;
    }

    if(curr_count == 2){
        clicks    = -1;
        TIME_LEFT = GAME_TIME;
        started   = 0;
        StartScreen();
        int registered = 0;
        return;
    }

    lcd.clear();
    lcd.print("Goodbye!");
    exit(0);
}

void loop() 
{
  //Starts timer after inital click
  if(started == 1)
    if(Timer(0))
      FinishedScreen();
      
  if(ClickRegistered()){
    if(started == 0){//Registers inital click
      started = 1;
      TIME_LEFT++;
    }
    
    clicks += 1;
    lcd.clear();
    lcd.setCursor(8,1);
    lcd.print(clicks);
   }
}


